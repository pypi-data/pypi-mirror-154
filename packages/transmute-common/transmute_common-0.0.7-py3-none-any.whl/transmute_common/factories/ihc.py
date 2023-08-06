def create(values = None):
  record = {
    "test": None,
    "value": None,
    "interpretation": None,
    "threshold": None,
    "component": None,
    "gene": None,
    "genomicSource": None,
    "equivocal": None,
    "therapyRecommendation": None,
    "expressionType": None,
    "intensity": None,
    "stainPercent": None,
    "result": None,
  }
  if values!=None:
    record.update(values)
  return record
