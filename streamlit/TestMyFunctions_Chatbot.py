import unittest
import chatbot

class TestMyFunctions_Chatbot(unittest.TestCase):
    locations = ["Bancroft and Area", "Barrie And District", "Brantford Region", "Cambridge", "Greater Toronto", "Grey Bruce Owen Sound", "Guelph And District", "Hamilton Burlington", "Huron Perth", "Kawartha Lakes", "Kingston And Area", "Kitchener Waterloo", "Lakelands", "London St Thomas", "Mississauga", "Niagara Region", "Northumberland Hills", "North Bay", "Oakville Milton", "Ottawa", "Peterborough And Kawarthas", "Quinte And District", "Rideau St Lawrence", "Sault Ste Marie", "Simcoe And District", "Sudbury", "Tillsonburg District" , "Windsor Essex" , "Woodstock Ingersoll"]
    building_types = ['Composite', 'Single Family', 'One Storey', 'Two Storey', 'Townhouse', 'Apartment']

    def test_bancroft_single_family(self):
        if chatbot.get_data_by_region_bldg_date(self.locations[0], self.building_types[1]) == 'PRED_Bancroft_and_Area_Benchmark_SA_SINGLE_FAMILY':
            pass

    def test_barrie_two_storey(self):
        if chatbot.get_data_by_region_bldg_date(self.locations[1], self.building_types[2]) == 'PRED_Barrie_And_Distinct_Benchmark_SA_TWO_STOREY':
            pass

    def test_brantford_townhouse(self):
        if chatbot.get_data_by_region_bldg_date(self.locations[2], self.building_types[4]) == 'PRED_Brantford_Region_Benchmark_SA_TOWNHOUSE':
            pass