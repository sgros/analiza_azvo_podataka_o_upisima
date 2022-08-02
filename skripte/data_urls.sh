#!/bin/bash

# Podaci se dohvacaju sa stranice https://www.studij.hr/statistika

rm -rf data/
mkdir data/

wget -O data/2022l.xls "https://www.studij.hr/public/resources/attractiveness_of_study_programs/excel_tables/2022%20ljetni%20rok.xls"
wget -O data/2022j.xls "https://www.studij.hr/public/resources/brosure/tablice/2022 jesenski rok.xls"
wget -O data/2021l.xls "https://www.studij.hr/public/resources/brosure/tablice/21_7_2021.xls"
wget -O data/2021j.xls "https://www.studij.hr/public/resources/brosure/tablice/2021 jesenski rok.xls"
wget -O data/2020l.xls "https://www.studij.hr/public/resources/brosure/tablice/2020 ljetni rok.xls"
wget -O data/2020j.xls "https://www.studij.hr/public/resources/brosure/tablice/Jesenski%20rok%202020.xls"
wget -O data/2019l.xls "https://www.studij.hr/public/resources/brosure/tablice/2019 ljetni rok.xls"
wget -O data/2019j.xls "https://www.studij.hr/public/resources/brosure/tablice/2019 jesenski rok.xls"
wget -O data/2018l.xls "https://www.studij.hr/public/resources/brosure/tablice/2018 ljetni rok.xls"
wget -O data/2018j.xls "https://www.studij.hr/public/resources/brosure/tablice/2018 jesenski rok.xls"
wget -O data/2017l.xls "https://www.studij.hr/public/resources/brosure/tablice/2017 ljetni rok.xls"
wget -O data/2017j.xls "https://www.studij.hr/public/resources/brosure/tablice/2017 jesenski rok.xls"
wget -O data/2016l.xls "https://www.studij.hr/public/resources/brosure/tablice/2016 ljetni rok.xls"
wget -O data/2016j.xls "https://www.studij.hr/public/resources/brosure/tablice/2016 jesenski rok.xls"
wget -O data/2015l.xls "https://www.studij.hr/public/resources/brosure/tablice/2015 ljetni rok.xls"
wget -O data/2015j.xls "https://www.studij.hr/public/resources/brosure/tablice/2015 jesenski rok.xls"
wget -O data/2014l.xls "https://www.studij.hr/public/resources/brosure/tablice/2014 ljetni rok.xls"
wget -O data/2014j.xls "https://www.studij.hr/public/resources/brosure/tablice/2014 jesenski rok.xls"
wget -O data/2013l.xls "https://www.studij.hr/public/resources/brosure/tablice/2013 ljetni rok.xls"
wget -O data/2013j.xls "https://www.studij.hr/public/resources/brosure/tablice/2013 jesenski rok.xls"
wget -O data/2012l.xls "https://www.studij.hr/public/resources/brosure/tablice/2012 ljetni rok.xls"
wget -O data/2012j.xls "https://www.studij.hr/public/resources/brosure/tablice/2012 jesenski rok.xls"
wget -O data/2011l.xls "https://www.studij.hr/public/resources/brosure/tablice/2011 ljetni rok.xls"
wget -O data/2011j.xls "https://www.studij.hr/public/resources/brosure/tablice/2011 jesenski rok.xls"
wget -O data/2010l.xls "https://www.studij.hr/public/resources/brosure/tablice/2010 ljetni rok.xls"
wget -O data/2010j.xls "https://www.studij.hr/public/resources/brosure/tablice/2010 jesenski rok.xls"
