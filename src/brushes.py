from valvevmf import VmfNode

def make_world(bsp):
    hid = 1
    world = VmfNode('world', [('id', hid), ('classname', 'worldspawn')])

    def _find_bside_oface():
        return None

    def _convert_plane(bspPlane):
        return ((0,0,0), (0,0,0), (0,0,0))

    def dot_product(A,B):
        return sum([A[i]*B[i] for i in range(3)])

    def _texinfo_convert(texinfo, origin=None):
        # this is more or less a reverse implementation of source's mp/src/utils/vbsp/textures.cpp
        if origin is None:
            origin = (0,0,0) # assume worldspawn

        shift = (texinfo.textureVecsTexelsPerWorldUnits[0][3] - dot_product(origin, texinfo.textureVecsTexelsPerWorldUnits[0]),
                texinfo.textureVecsTexelsPerWorldUnits[1][3] - dot_product(origin, texinfo.textureVecsTexelsPerWorldUnits[1]))
        shiftScale = ((texinfo.lightmapVecsLuxelsPerWorldUnits[0][3] - dot_product(origin, texinfo.lightmapVecsLuxelsPerWorldUnits[0])) / (shift[0] or 1),
                    (texinfo.lightmapVecsLuxelsPerWorldUnits[1][3] - dot_product(origin, texinfo.lightmapVecsLuxelsPerWorldUnits[1])) / (shift[1] or 1))
        
        textureWorldUnitsPerTexel = [0.25, 0.25] # ????? we're guessing here
        lightmapWorldUnitsPerLuxel = shiftScale[0] / textureWorldUnitsPerTexel[0]
        lightmapscale = 1 / lightmapWorldUnitsPerLuxel if lightmapWorldUnitsPerLuxel else 16

        uaxis = [0, 0, 0, shift[0], textureWorldUnitsPerTexel[0]]
        vaxis = [0, 0, 0, shift[1], textureWorldUnitsPerTexel[1]]
        for i in range(3):
            uaxis[i] = texinfo.textureVecsTexelsPerWorldUnits[0][i] * textureWorldUnitsPerTexel[0]
            vaxis[i] = texinfo.textureVecsTexelsPerWorldUnits[1][i] * textureWorldUnitsPerTexel[1]
        return uaxis, vaxis, lightmapscale

    for brush in bsp[18]:
        solid = VmfNode('solid', [('id', hid)])
        for sideNum in range(brush.firstSide, brush.firstSide + brush.numSides):
            brushSide = bsp[19][sideNum]
            bspPlane = bsp[1][brushSide.planeNum]
            texInfo = bsp[6][brushSide.texInfo]
            texData = bsp[2][texInfo.texData]

            hplane = _convert_plane(bspPlane)
            uaxis, vaxis, lightmapscale = _texinfo_convert(texInfo)
            face = _find_bside_oface()

            if brushSide.dispInfo != -1:
                bspdisp = bsp[26][brushSide.dispInfo]

            hid += 1
            side = VmfNode('side', [('id', hid)])

            side.properties.append(('plane', hplane))
            side.properties.append(('material', bsp[43][texData.nameStringTableID]))

            side.properties.append(('uaxis', uaxis))
            side.properties.append(('vaxis', vaxis))

            side.properties.append(('rotation', 0))
            side.properties.append(('lightmapscale', lightmapscale))
            if face:
                side.properties.append(('smoothing_groups', face.smoothingGroup))
            else:
                side.properties.append(('smoothing_groups', 0))


            solid.nodes.append(side)

        world.nodes.append(solid)
    return world