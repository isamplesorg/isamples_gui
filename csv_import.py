from frictionless import Package, Resource

SCHEMA_JSON = {
  "fields": [
    {
      "type": "string",
      "name": "id"
    },
    {
      "type": "string",
      "name": "label"
    },
    {
      "type": "string",
      "name": "description"
    },
    {
      "type": "array",
      "name": "hasContextCategory"
    },
    {
      "type": "array",
      "name": "hasMaterialCategory"
    },
    {
      "type": "array",
      "name": "hasSpecimenCategory"
    },
    {
      "type": "array",
      "name": "keywords"
    },
    {
      "type": "array",
      "name": "informalClassification"
    },
    {
      "type": "string",
      "name": "producedBy_label"
    },
    {
      "type": "string",
      "name": "producedBy_description"
    },
    {
      "type": "string",
      "name": "producedBy_hasFeatureOfInterest"
    },
    {
      "type": "array",
      "name": "producedBy_responsibility"
    },
    {
      "type": "datetime",
      "name": "producedBy_resultTime"
    },
    {
      "type": "string",
      "name": "producedBy_samplingSite_description"
    },
    {
      "type": "string",
      "name": "producedBy_samplingSite_label"
    },
    {
      "type": "integer",
      "name": "producedBy_samplingSite_location_elevationInMeters"
    },
    {
      "type": "number",
      "name": "producedBy_samplingSite_location_latitude"
    },
    {
      "type": "number",
      "name": "producedBy_samplingSite_location_longitude"
    },
    {
      "type": "array",
      "name": "producedBy_samplingSite_placeName"
    },
    {
      "type": "array",
      "name": "registrant"
    },
    {
      "type": "array",
      "name": "samplingPurpose"
    },
    {
      "type": "string",
      "name": "curation_label"
    },
    {
      "type": "string",
      "name": "curation_description"
    },
    {
      "type": "string",
      "name": "curation_accessContraints"
    },
    {
      "type": "string",
      "name": "curation_location"
    },
    {
      "type": "string",
      "name": "curation_responsibility"
    },
    {
      "type": "array",
      "name": "compliesWith"
    },
    {
      "type": "array",
      "name": "authorizedBy"
    }
  ]
}


def create_isamples_package(file_path: str) -> Package:
  """
  Opens the specified file and return it as a list of iSamples Core record dictionaries
  Args:
      file_path: The path to the file to open

  Returns: A list of dictionaries containing the records
  """
  data_resource = Resource(source=file_path, schema=SCHEMA_JSON, trusted=True)
  package = Package(resources=[data_resource], name="isamples", title="isamples", id="isamples", trusted=True)
  return package
