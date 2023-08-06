def create(values = None):
  record = {
    "name": None,
    "5pGene": None,
    "5pExon": None,
    "5pChrom": None,
    "5pPos": None,
    "3pGene": None,
    "3pExon": None,
    "3pChrom": None,
    "3pPos": None,
    "support": None,
    "frame": None,
    "read_count": None,
    "normalizedExpression": None,
    "normalization": None,
    "frame": None,
    "interpretation": None,
    "therapyRecommendation": None,
  }
  if values!=None:
    record.update(values)
  return record
