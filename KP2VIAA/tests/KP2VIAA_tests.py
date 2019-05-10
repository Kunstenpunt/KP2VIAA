#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest import TestCase
from pandas import DataFrame
from KP2VIAA.KP2VIAA import KP2VIAA
from json import load
from codecs import open
from lxml import etree
import os


class KP2VIAATests(TestCase):
    def setUp(self):
        self.kp2viaa = KP2VIAA(path_to_dbcfg="../resources/db.cfg",
                               path_to_viaa2kp="../resources/viaa_id_testcase.json",
                               path_metadata_mapping="../resources/metadata_mapping.json",
                               path_genres_mapping="../resources/genres_mapping.json",
                               path_languages_mapping="../resources/languages_mapping.json",
                               path_to_qas_auth="../resources/qasviaaauthenticationbase64.txt",
                               path_to_xsd="../resources/viaa_metadatamodel_van_viaa_naar_mam.xsd",
                               path_to_pass_viaa="../resources/pass_viaa.txt")
        self.maxDiff = None

    def test_get_kunstenpunt_productie_id(self):
        self.kp2viaa.get_kunstenpunt_productie_id("bv79s1r49d")
        self.assertEqual(self.kp2viaa.viaa_id_to_kp_productie_show_id_mapping["bv79s1r49d"]["kp_productie_id"], 429013)

    def test_map_kp_general_to_dc_titles(self):
        self.kp2viaa.read_mapping_viaa_to_kp()
        self.kp2viaa.get_kp_metadata_general_for_viaa_id("viaa_id")
        self.kp2viaa.create_viaa_xml()
        self.kp2viaa.ensure_element_exists("dc_titles")
        self.kp2viaa.write_kp_general_to_update_tree()
        self.assertTrue(len(self.kp2viaa.update_tree.xpath("//seizoen")), 1)
        print(etree.tostring(self.kp2viaa.update_tree, pretty_print=True))

    def test_ensure_element_exists(self):
        self.kp2viaa.create_viaa_xml()
        self.kp2viaa.ensure_element_exists("testje")
        self.assertEqual(len(self.kp2viaa.update_tree.xpath("//testje")), 1)

    def test_map_kp_persons_to_viaa_makers(self):
        self.kp2viaa.consume_api("bv79s1r49d")
        self.kp2viaa.read_mapping_viaa_to_kp()
        self.kp2viaa.get_kp_metadata_personen_for_viaa_id("viaa_id")
        self.kp2viaa.create_viaa_xml()
        self.kp2viaa.ensure_element_exists("dc_creators")
        self.kp2viaa.write_kp_persons_to_viaa_makers()
        self.assertEqual(self.kp2viaa.update_tree.xpath("//Choreograaf")[0].text, "Anne Teresa De Keersmaeker")

    def test_map_kp_persons_to_viaa_contributors(self):
        self.kp2viaa.read_mapping_viaa_to_kp()
        self.kp2viaa.get_kp_metadata_personen_for_viaa_id("viaa_id")
        self.kp2viaa.create_viaa_xml()
        self.kp2viaa.ensure_element_exists('dc_contributors')
        self.kp2viaa.write_kp_persons_to_viaa_contributors()
        self.assertEqual(self.kp2viaa.update_tree.xpath("//Dirigent")[0].text, "Philippe Herreweghe")

    def test_map_kp_organisations_to_viaa_makers(self):
        self.kp2viaa.read_mapping_viaa_to_kp()
        self.kp2viaa.get_kp_metadata_organisaties_for_viaa_id("viaa_id")
        self.kp2viaa.create_viaa_xml()
        self.kp2viaa.ensure_element_exists('dc_creators')
        self.kp2viaa.write_kp_organisations_to_viaa_makers()
        self.assertEqual(self.kp2viaa.update_tree.xpath("//Maker")[0].text, "Rosas")
        print(etree.tostring(self.kp2viaa.update_tree, pretty_print=True))

    def test_map_kp_organisations_to_viaa_contributors(self):
        self.kp2viaa.read_mapping_viaa_to_kp()
        self.kp2viaa.get_kp_metadata_organisaties_for_viaa_id("viaa_id")
        self.kp2viaa.create_viaa_xml()
        self.kp2viaa.ensure_element_exists('dc_contributors')
        self.kp2viaa.write_kp_organisations_to_viaa_contributors()
        print(etree.tostring(self.kp2viaa.update_tree, pretty_print=True))

    def test_map_kp_genres_to_viaa_genres(self):
        self.kp2viaa.read_mapping_viaa_to_kp()
        self.kp2viaa.get_kp_metadata_genres_for_viaa_id("viaa_id")
        self.kp2viaa.create_viaa_xml()
        self.kp2viaa.ensure_element_exists('dc_types')
        self.kp2viaa.write_kp_genres_to_viaa_genres()
        print(etree.tostring(self.kp2viaa.update_tree, pretty_print=True))

    def test_map_kp_languages_to_viaa_languages(self):
        self.kp2viaa.read_mapping_viaa_to_kp()
        self.kp2viaa.get_kp_metadata_languages_for_viaa_id("viaa_id")
        self.kp2viaa.create_viaa_xml()
        self.kp2viaa.ensure_element_exists("dc_languages")
        self.kp2viaa.write_kp_languages_to_viaa_languages()
        print(etree.tostring(self.kp2viaa.update_tree, pretty_print=True))

    def test_write_all(self):
        self.kp2viaa.read_mapping_viaa_to_kp()
        self.kp2viaa.get_kp_metadata_personen_for_viaa_id("viaa_id")
        self.kp2viaa.get_kp_metadata_general_for_viaa_id("viaa_id")
        self.kp2viaa.get_kp_metadata_organisaties_for_viaa_id("viaa_id")
        self.kp2viaa.get_kp_metadata_genres_for_viaa_id("viaa_id")
        self.kp2viaa.get_kp_metadata_languages_for_viaa_id("viaa_id")
        self.kp2viaa.consume_api("bv79s1r49d")
        self.kp2viaa.create_viaa_xml()
        self.kp2viaa.ensure_element_exists("dc_titles")
        self.kp2viaa.ensure_element_exists('dc_creators')
        self.kp2viaa.ensure_element_exists('dc_contributors')
        self.kp2viaa.ensure_element_exists('dc_types')
        self.kp2viaa.ensure_element_exists("dc_languages")
        self.kp2viaa.write_kp_general_to_update_tree()
        self.kp2viaa.write_kp_persons_to_viaa_makers()
        self.kp2viaa.write_kp_persons_to_viaa_contributors()
        self.kp2viaa.write_kp_organisations_to_viaa_makers()
        self.kp2viaa.write_kp_organisations_to_viaa_contributors()
        self.kp2viaa.write_kp_languages_to_viaa_languages()
        self.kp2viaa.write_kp_genres_to_viaa_genres()
        #print(etree.tostring(self.kp2viaa.update_tree, pretty_print=True, encoding="utf-8"))

    def test_encoding(self):
        self.kp2viaa.read_mapping_viaa_to_kp()
        self.kp2viaa.get_kp_metadata_personen_for_viaa_id("viaa_id")
        encoded_name = self.kp2viaa.people_info.ix[18]["full name"]
        self.kp2viaa.create_viaa_xml()
        child = etree.Element("test")
        child.text = encoded_name #.decode("utf-8")
        self.kp2viaa.update_tree.append(child)
        #print(etree.tostring(self.kp2viaa.update_tree, pretty_print=True, encoding="utf-8"))

    def test_read_mapping(self):
        self.kp2viaa.read_mapping_viaa_to_kp()
        expected_mapping = {
            "viaa_id": {
                "kp_productie_id": 429013,
                "kp_show_id": "kp_show_id"
            }
        }
        self.assertDictEqual(self.kp2viaa.viaa_id_to_kp_productie_show_id_mapping, expected_mapping)

    def test_dbcfg_read_in_correctly(self):
        self.assertEqual(self.kp2viaa.path_to_dbcfg, "../resources/db.cfg")
        self.assertTrue("db" in self.kp2viaa.cfg)

    def test_get_metadata_for_mozart(self):
        self.kp2viaa.read_mapping_viaa_to_kp()
        self.kp2viaa.get_kp_metadata_general_for_viaa_id("viaa_id")
        mozart_metadata_expected = DataFrame([
            {
                "name": "Mozart/Concert Arias Un Moto di Gioia",
                "season": "1992-1993",
                "rerun": None
            }
        ], columns=["name", "season", "rerun"])
        self.assertTrue(self.kp2viaa.general_info.equals(mozart_metadata_expected))

    def test_get_metadata_for_mozart_functies_personen(self):
        self.kp2viaa.read_mapping_viaa_to_kp()
        self.kp2viaa.get_kp_metadata_personen_for_viaa_id("viaa_id")
        with open("../resources/mozart_personen_functies.json", "r", "utf-8") as f:
            x = load(f, encoding='utf-8')
        mozart_metadata_expected = DataFrame(data=x, columns=['full name', "function", 'production id'])
        self.assertEqual(self.kp2viaa.people_info.to_string(), mozart_metadata_expected.to_string())

    def test_get_metadata_for_mozart_organisaties(self):
        self.kp2viaa.read_mapping_viaa_to_kp()
        self.kp2viaa.get_kp_metadata_organisaties_for_viaa_id("viaa_id")
        mozart_metadata_expected = DataFrame([
            {
                "organisation": "Rosas",
                "function": "gezelschap"
            }
        ], columns=["organisation", "function"])
        self.assertTrue(self.kp2viaa.organisations_info.equals(mozart_metadata_expected))

    def test_get_metadata_for_mozart_genres(self):
        self.kp2viaa.read_mapping_viaa_to_kp()
        self.kp2viaa.get_kp_metadata_genres_for_viaa_id("viaa_id")
        mozart_metadata_expected = DataFrame([
            {
                "show" : "Mozart/Concert Arias Un Moto di Gioia",
                "genre" : "dans"
            }
        ], columns=["show", "genre"])
        self.assertTrue(self.kp2viaa.genre_info.equals(mozart_metadata_expected))

    def test_get_metadata_for_mozart_languages(self):
        self.kp2viaa.read_mapping_viaa_to_kp()
        self.kp2viaa.get_kp_metadata_languages_for_viaa_id("viaa_id")
        mozart_metadata_expected = DataFrame([
            {
                "show" : "Mozart/Concert Arias Un Moto di Gioia",
                "language" : None
            }
        ], columns=["show", "language"])
        self.assertTrue(self.kp2viaa.language_info.equals(mozart_metadata_expected))

    def test_consume_api(self):
        #self.kp2viaa.consume_api("d9e8142d64714b2ab9081317f7ef0c64a33b914162b34b25a5ab91ba192181c744fb015640ec43c9be820ab05ad4a42e")
        self.kp2viaa.consume_api("bv79s1r49d")
        print(etree.tostring(self.kp2viaa.mediahaven_xml, pretty_print=True))

    def test_test_PID(self):
        test_api_output = etree.fromstring("""<searchResult><totalNrOfResults>2</totalNrOfResults></searchResult>""")
        self.kp2viaa.mediahaven_xml = test_api_output
        with self.assertRaises(Exception) as context:
            self.kp2viaa.test_if_pid_unique()
        self.assertEquals("'multiple items found in viaa for pid'", str(context.exception))

    # def test_validate_kp_input_to_viaa_xsd(self):     Unfinished: XSD VIAA does not match VIAA metadatamodel
    #
    #     self.test_write_all()
    #     self.kp2viaa.validate_updated_tree_to_VIAA_xsd()
    #     self.assertTrue(self.kp2viaa.validate_updated_tree_to_VIAA_xsd())

    def test_get_mediahaven_fragmentID(self):
        self.kp2viaa.consume_api("bv79s1r49d")
        id = self.kp2viaa.get_mediahaven_fragmentId()
        self.assertEqual(id, "d9e8142d64714b2ab9081317f7ef0c64a33b914162b34b25a5ab91ba192181c744fb015640ec43c9be820ab05ad4a42e")

    def test_write_to_xml(self):

        self.test_write_all()
        self.kp2viaa.write_tree_to_xml()
        self.assertTrue(os.path.exists("../resources/xml_viaa.xml"))

    def test_remove_file(self):

        self.kp2viaa.remove_viaa_xml_file()
        self.assertFalse(os.path.exists("../resources/xml_viaa.xml"))

    def test_send_payload_to_viaa(self):

        self.test_write_all()
        self.kp2viaa.write_tree_to_xml()
        self.kp2viaa.send_update_tree_to_viaa()
