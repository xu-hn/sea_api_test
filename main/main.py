# coding = utf-8
import sys
sys.path.append('../')
from case.sea_api_test import SeaclassTestCase

if __name__ == '__main__':
   
    app = SeaclassTestCase()
    app.runAllCase("SEA")



