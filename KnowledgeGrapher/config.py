#Database configuration
dbURL = "localhost"
dbPort = 7687
dbUser="neo4j"
dbPassword = "bioinfo1112"
########################
dataDirectory = "/Users/albertosantos/Development/Clinical_Proteomics_Department/ClinicalKnowledgeGraph(CKG)/data"
#Import directory
importDirectory = dataDirectory + "/imports"
#Datasets directory
datasetsImportDirectory = importDirectory + "/datasets/"
#Imports 
entities = ["Disease","Drug","Tissue","Biological_process", "Molecular_function", "Cellular_compartment", "PTM", "Clinical_variable"]
#Database resources
PPI_resources = ["IntAct"]
disease_resources = [("Protein","DisGEnet"),("Known_variant","CGI"),("Known_variant","OncoKB")]
drug_resources = ["DGIdb","CGI","OncoKB"]
variant_resources = ["CGI","OncoKB"]
pathway_resources = ["Reactome"]

#Internal Databases entities
internalEntities = [("Protein","Disease"), ("Protein", "Tissue"), ("Protein","Cellular_compartment")]

#Mentions entities
mentionEntities = ["Disease", "Tissue", "Protein", "Cellular_compartment", "Chemical"]

#Analyses configuration
similarityMeasures = ["pearson"]
########################

mappingFile = dataDirectory + "/ontologies/mapping.tsv"

#Dataset types
datasetsDirectory = dataDirectory + "/experiments/"
#Proteomics
clinicalDirectory = datasetsDirectory + "PROJECTID/clinical/"
proteomicsDirectory = datasetsDirectory + "PROJECTID/proteomics/"
genomicsDirectory = datasetsDirectory + "PROJECTID/wes/"
dataTypes = {"clinical":{"directory":clinicalDirectory,
                            "file":"clinicalData.xlsx"},
            "proteomics":{"directory": proteomicsDirectory,
                            "proteins":{"columns":
                                            ["Majority protein IDs",
                                            "Gene names", "Q-value", 
                                            "Score", 
                                            "LFQ intensity \d+_AS\d+_?\d*",  #subject_replicate_timepoint
                                            "Reverse",
                                            "Potential contaminant",
                                            "Only identified by site"],
                                        "filters" : ["Reverse",
                                                        "Potential contaminant",
                                                        "Only identified by site"],
                                        "proteinCol" : "Majority protein IDs",
                                        "valueCol" : "LFQ intensity",
                                        "indexCol" : "Majority protein IDs",
                                        "log": "log10",
                                        "file": "proteinGroups.txt"},
                            "peptides":{"columns":
                                            ["Sequence",
                                            "Amino acid before",
                                            "First amino acid",
                                            "Second amino acid",
                                            "Second last amino acid",
                                            "Last amino acid",
                                            "Amino acid after", 
                                            "Proteins", 
                                            "Start position",
                                            "End position",
                                            "Score", 
                                            "Intensity \d+_AS\d+_?\d*", 
                                            "Reverse",
                                            "Potential contaminant"],
                                        "filters" : ["Reverse",
                                                        "Potential contaminant"],
                                        "proteinCol" : "Proteins",
                                        "valueCol" : "Intensity",
                                        "indexCol" : "Sequence",
                                        "positionCols":["Start position","End position"],
                                        "type": "tryptic peptide",
                                        "log": "log10",
                                        "file":"peptides.txt"},
                            "Oxydation(M)":{"columns":
                                            ["Proteins",
                                            "Positions within proteins", 
                                            "Amino acid",
                                            "Sequence window",
                                            "Score", 
                                            "Intensity \d+_\d+", 
                                            "Reverse",
                                            "Potential contaminant"],
                                        "filters" : ["Reverse",
                                                        "Potential contaminant"],
                                        "proteinCol" : "Proteins",
                                        "indexCol" : "Proteins",
                                        "valueCol" : "Intensity",
                                        "multipositions": "Positions within proteins",
                                        "positionCols": ["Positions within proteins","Amino acid"],
                                        "sequenceCol": "Sequence window",
                                        "modId":"MOD:00256",
                                        "geneCol":"Gene names",
                                        "log": "log10",
                                        "file":"Oxidation (M)Sites.txt"},
                            "Glycation":{"columns":
                                            ["Proteins",
                                            "Positions within proteins", 
                                            "Amino acid",
                                            "Sequence window",
                                            "Score", 
                                            "Intensity \d+_\d+", 
                                            "Reverse",
                                            "Potential contaminant"],
                                        "filters" : ["Reverse",
                                                        "Potential contaminant"],
                                        "proteinCol" : "Proteins",
                                        "indexCol" : "Proteins",
                                        "valueCol" : "Intensity",
                                        "multipositions": "Positions within proteins",
                                        "positionCols": ["Positions within proteins","Amino acid"],
                                        "sequenceCol": "Sequence window",
                                        "modId":"MOD:00764",
                                        "geneCol":"Gene names",
                                        "log": "log10",
                                        "file":"GlycationSites.txt"}
                            },
            "PTMData":{"columns" : 
                            ["Protein", "Positions", 
                                "Amino acid", "Intensity \d+_\d+", 
                                "Reverse", "Potential contaminant"],
                            "filters" : ["Reverse", "Potential contaminant"],
                            "proteinCol" : "Protein",
                            "log": "log10"
                            },
            "wes":{"directory": genomicsDirectory,
                        "columns" : ["Chr", "Start", "Ref", "Alt", 
                                    "Func.refGene", "Gene.refGene", 
                                    "ExonicFunc.refGene", "AAChange.refGene", 
                                    "Xref.refGene", "SIFT_score", "SIFT_pred", "Polyphen2_HDIV_score",
                                    "Polyphen2_HDIV_pred", "Polyphen2_HVAR_score",
                                    "Polyphen2_HVAR_pred", "LRT_score", "LRT_pred",
                                    "MutationTaster_score", "MutationTaster_pred",
                                    "MutationAssessor_score", "MutationAssessor_pred",
                                    "FATHMM_score", "FATHMM_pred", "PROVEAN_score",
                                    "PROVEAN_pred", "VEST3_score", "CADD_raw", "CLINSIG",
                                    "CLNDBN", "CLNACC", "CLNDSDB", "CLNDSDBID", "cosmic70", 
                                    "ICGC_Id", "ICGC_Occurrence"],
                        "position" : "Start",
                        "id_fields" : ["Chr", "Start", "Ref", "Alt"],
                        "alt_names" : "AAChange.refGene",
                        "somatic_mutation_attributes":["chr", "position", "reference", "alternative",
                                    "region", "gene",
                                    "function", "Xref", 
                                    "SIFT_score", "SIFT_pred", "Polyphen2_HDIV_score",
                                    "Polyphen2_HDIV_pred", "Polyphen2_HVAR_score",
                                    "Polyphen2_HVAR_pred", "LRT_score", "LRT_pred",
                                    "MutationTaster_score", "MutationTaster_pred",
                                    "MutationAssessor_score", "MutationAssessor_pred",
                                    "FATHMM_score", "FATHMM_pred", "PROVEAN_score",
                                    "PROVEAN_pred", "VEST3_score", "CADD_raw", "CLINSIG",
                                    "CLNDBN", "CLNACC", "CLNDSDB", "CLNDSDBID", "cosmic70", 
                                    "ICGC_Id", "ICGC_Occurrence", "alternative_names","ID"],
                        "new_columns": ["chr", "position", "reference", "alternative",
                                    "region", "gene",
                                    "function", "Xref", 
                                    "SIFT_score", "SIFT_pred", "Polyphen2_HDIV_score",
                                    "Polyphen2_HDIV_pred", "Polyphen2_HVAR_score",
                                    "Polyphen2_HVAR_pred", "LRT_score", "LRT_pred",
                                    "MutationTaster_score", "MutationTaster_pred",
                                    "MutationAssessor_score", "MutationAssessor_pred",
                                    "FATHMM_score", "FATHMM_pred", "PROVEAN_score",
                                    "PROVEAN_pred", "VEST3_score", "CADD_raw", "CLINSIG",
                                    "CLNDBN", "CLNACC", "CLNDSDB", "CLNDSDBID", "cosmic70", 
                                    "ICGC_Id", "ICGC_Occurrence", "sample", "variantCallingMethod", "annotated", "alternative_names", "ID"],
                        "types" :{"Somatic_mutation": "KEEP", "Germline_mutation": "REJECT"}                       
                }
        }
###Variant sources
'''
COSMIC
dbNSFP
dbSNP
Linkage-Physical Map
Database of Genomic Variants
Exome Sequencing Project
gwasCatalog
HapMap
Thousand Genomes
'''
#####
