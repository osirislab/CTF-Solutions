import math

def calculate(sequence):
  m = []
  for i in range(1,10):
    m.append(math.log10(1+1.0/i))

  nums = [x[0] for x in sequence.split(",")]

  o = {}

  for num in nums:
    if num in o:
      o[num] += 1
    else:
      o[num] = 1
  
  if len(o) != 9: return False

  else:
    for d in sorted(o):
      if not (float(o[d]) / sum([int(x) for x in o.values()]) >= m[int(d)-1] - 0.05 and float(o[d]) / sum([int(x) for x in o.values()]) <= m[int(d)-1] + 0.05):
	return False
  return True
