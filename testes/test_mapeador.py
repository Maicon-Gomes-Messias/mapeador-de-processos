# -*- coding: utf-8 -*-
"""Testes do mapeador de processos.

Rode a partir da raiz do projeto:

    python -m unittest discover -s testes -v
"""

import sys
import tempfile
import unittest
from pathlib import Path
from xml.etree import ElementTree as ET

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import mapeador  # noqa: E402

NS = {
    "bpmn": "http://www.omg.org/spec/BPMN/20100524/MODEL",
    "bpmndi": "http://www.omg.org/spec/BPMN/20100524/DI",
}


def processo_exemplo() -> dict:
    return {
        "processo": {"nome": "Processo de teste"},
        "raias": ["Área A", "Área B"],
        "etapas": [
            {"id": "inicio", "nome": "Começo", "tipo": "inicio", "raia": "Área A"},
            {"id": "t1", "nome": "Primeira tarefa", "tipo": "tarefa", "raia": "Área A",
             "tempo_min": 10, "proximo": ["g1"]},
            {"id": "g1", "nome": "Decide?", "tipo": "decisao", "raia": "Área A",
             "proximo": ["t2", "fim"], "rotulos": {"t2": "Sim", "fim": "Não"}},
            {"id": "t2", "nome": "Segunda tarefa", "tipo": "tarefa", "raia": "Área B",
             "tempo_min": 20, "espera_min": 60, "automatizavel": True, "proximo": ["fim"]},
            {"id": "fim", "nome": "Fim", "tipo": "fim", "raia": "Área B"},
        ],
    }


class TesteValidacao(unittest.TestCase):
    def test_processo_valido_nao_tem_erros(self):
        self.assertEqual(mapeador.validar(processo_exemplo()), [])

    def test_id_repetido(self):
        p = processo_exemplo()
        p["etapas"].append({"id": "t1", "nome": "Repetida", "tipo": "tarefa", "raia": "Área A"})
        erros = mapeador.validar(p)
        self.assertTrue(any("repetidos" in e for e in erros), erros)

    def test_tipo_invalido(self):
        p = processo_exemplo()
        p["etapas"][1]["tipo"] = "banana"
        erros = mapeador.validar(p)
        self.assertTrue(any("tipo inválido" in e for e in erros), erros)

    def test_proximo_inexistente(self):
        p = processo_exemplo()
        p["etapas"][1]["proximo"] = ["nao_existe"]
        erros = mapeador.validar(p)
        self.assertTrue(any("não existe" in e for e in erros), erros)

    def test_raia_nao_declarada(self):
        p = processo_exemplo()
        p["etapas"][1]["raia"] = "Área C"
        erros = mapeador.validar(p)
        self.assertTrue(any("não está declarada" in e for e in erros), erros)

    def test_tempo_negativo(self):
        p = processo_exemplo()
        p["etapas"][1]["tempo_min"] = -5
        erros = mapeador.validar(p)
        self.assertTrue(any("≥ 0" in e for e in erros), erros)

    def test_proximo_implicito_e_preenchido(self):
        p = processo_exemplo()
        del p["etapas"][1]["proximo"]
        self.assertEqual(mapeador.validar(p), [])
        self.assertEqual(p["etapas"][1]["proximo"], ["g1"])


class TesteBpmn(unittest.TestCase):
    def setUp(self):
        self.processo = processo_exemplo()
        mapeador.validar(self.processo)
        self.xml = mapeador.gerar_bpmn(self.processo)
        self.raiz = ET.fromstring(self.xml)

    def test_xml_valido(self):
        self.assertTrue(self.raiz.tag.endswith("definitions"))

    def test_todos_os_fluxos_apontam_para_nos_existentes(self):
        ids = {e.get("id") for e in self.raiz.iter()}
        for fluxo in self.raiz.iter("{http://www.omg.org/spec/BPMN/20100524/MODEL}sequenceFlow"):
            self.assertIn(fluxo.get("sourceRef"), ids)
            self.assertIn(fluxo.get("targetRef"), ids)

    def test_flow_node_refs_existem(self):
        ids = {e.get("id") for e in self.raiz.iter()}
        for ref in self.raiz.iter("{http://www.omg.org/spec/BPMN/20100524/MODEL}flowNodeRef"):
            self.assertIn(ref.text, ids)

    def test_automatizavel_vira_service_task(self):
        self.assertEqual(len(list(self.raiz.iter(
            "{http://www.omg.org/spec/BPMN/20100524/MODEL}serviceTask"))), 1)

    def test_desenho_tem_formas_para_todos_os_nos(self):
        nos = {e.get("id") for e in self.raiz.iter()
               if e.tag.endswith(("Task", "Event", "Gateway"))}
        formas = {s.get("bpmnElement") for s in self.raiz.iter(
            "{http://www.omg.org/spec/BPMN/20100524/DI}BPMNShape")}
        self.assertTrue(nos.issubset(formas), nos - formas)

    def test_larguras_batem_com_os_tamanhos(self):
        # tarefa = 140x80
        forma = [s for s in self.raiz.iter(
            "{http://www.omg.org/spec/BPMN/20100524/DI}BPMNShape")
            if s.get("bpmnElement") == "t1"][0]
        limites = forma.find("{http://www.omg.org/spec/DD/20100524/DC}Bounds")
        self.assertEqual(limites.get("width"), "140")
        self.assertEqual(limites.get("height"), "80")


class TesteAnalise(unittest.TestCase):
    def test_indicadores(self):
        p = processo_exemplo()
        mapeador.validar(p)
        a = mapeador.analisar(p)
        self.assertEqual(a["etapas"], 5)
        self.assertEqual(a["tarefas"], 2)
        self.assertEqual(a["tempo_execucao"], 30)
        self.assertEqual(a["tempo_espera"], 60)
        self.assertEqual(a["lead_time"], 90)
        self.assertEqual(a["automatizaveis"], 1)
        # Área A -> Área B (t1->g1 fica na mesma área; g1->t2 muda)
        self.assertEqual(a["handoffs"], 2)

    def test_gargalo_e_a_etapa_com_maior_espera(self):
        p = processo_exemplo()
        mapeador.validar(p)
        a = mapeador.analisar(p)
        self.assertEqual([g["id"] for g in a["gargalos"]], ["t2"])


class TesteArquivos(unittest.TestCase):
    def test_gera_os_tres_arquivos(self):
        p = processo_exemplo()
        mapeador.validar(p)
        with tempfile.TemporaryDirectory() as tmp:
            res = mapeador.processar(p, "teste", Path(tmp))
            for chave in ("bpmn", "relatorio", "painel"):
                self.assertTrue(res[chave].exists(), chave)
                self.assertGreater(res[chave].stat().st_size, 100)


if __name__ == "__main__":
    unittest.main()
