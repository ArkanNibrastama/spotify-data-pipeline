module "resource_area" {
  source = "./resource_area"
}

module "staging_area" {
  source = "./data_stage"
}

module "data_source" {
  source = "./data_source"
}

module "data_warehouse" {
  source = "./data_warehouse"
}

module "data_lake" {
  source = "./data_lake"
}

module "etl" {
  source = "./etl_pipeline"
}