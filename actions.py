import uuid

def id_generator():
    return "{0}-{1}-{2}-{3}-{4}".format(uuid.uuid4().hex[:8],uuid.uuid4().hex[:4],uuid.uuid4().hex[:4],uuid.uuid4().hex[:4],uuid.uuid4().hex[:12])
