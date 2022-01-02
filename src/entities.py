from valvevmf import VmfNode

def make_entities(bsp):
    entities = []
    for ent in bsp[0]:
        entity = VmfNode('entity')
        for prop in ent:
            if prop[0] == 'hammerid':
                prop[0] = 'id'
            elif prop[0] == 'model':
                continue
        entity.properties.append(tuple(prop))
        entities.append(entity)
    return entities