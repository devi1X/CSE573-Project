# CSE573-Project
CSE573 Project

## Step 1: MetaMap Annotator (all steps have been done already. You do not have to do this anymore.)
* Download MetaMap main release from [here](https://metamap.nlm.nih.gov/MainDownload.shtml)
* Download the MetMap Java API from [here](https://metamap.nlm.nih.gov/JavaApi.shtml)
* Extract the contents of these files using `tar -xf [filename]` for both of the files.
* After these are extracted:
```
$ cd public_mm/
$ ./bin/install.sh
```
Make sure ```mmserver is generated.```
Run the servers
```
$ ./bin/wsdserverctl start
$ ./bin/skrmedpostctl start
$ ./bin/mmserver
```
`cd MetaMapAnnotator/dist/` and run
```
$ java -jar dist/MetaMapAnnotator.jar
```
The files generated here were moved to `scraper/`. Go to `scraper/data` and run `combine.py`
This generates `combinedData.csv` Note that the Drugs, PatientsInfo, and Webmd files were also generated.

## (This step is very time consuming and has already been done. This does not need to be done anymore.) All of the necessary data in the entire project can be found in the csv files of `scraper/data/*.csv` or `src/`


## Step 2

The current `ontology/` direction contains the sql commands for building a database from the `csv` data.
Please examine the the `ontology/final` directory. Convert these to plaintext. All of these files can be converted into `csv` files. After we converted this into `csv` files. 
For example, `ontology/final/ontology_diseases.sql`:
```INSERT INTO ontology.diseases (disease_id, disease_name, description, records_count, has_symptom_count, has_treatment_count) VALUES ('C0000833', 'Abscess', 'new', 23, 4, 8);
INSERT INTO ontology.diseases (disease_id, disease_name, description, records_count, has_symptom_count, has_treatment_count) VALUES ('C0001125', 'Acidosis| Lactic', 'new', 12, 5, 2);
INSERT INTO ontology.diseases (disease_id, disease_name, description, records_count, has_symptom_count, has_treatment_count) VALUES ('C0001144', 'Acne Vulgaris', 'new', 168, 35, 33);
INSERT INTO ontology.diseases (disease_id, disease_name, description, records_count, has_symptom_count, has_treatment_count) VALUES ('C0001175', 'Acquired Immunodeficiency Syndrome', 'new', 9, 1, 2);
```
can be easily converted into
```angular2html
disease_id, disease_name, description, records_count, has_symptom_count, has_treatment_count
'C0001125', 'Acidosis| Lactic', 'new', 12, 5, 2
'C0001144', 'Acne Vulgaris', 'new', 168, 35, 33
'C0001175', 'Acquired Immunodeficiency Syndrome', 'new', 9, 1, 2
```

We can do this by using a script.
