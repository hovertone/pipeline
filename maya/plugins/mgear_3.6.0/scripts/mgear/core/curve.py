"""NurbsCurve creation functions"""

# TODO: Finish documentation

#############################################
# GLOBAL
#############################################
import pymel.core as pm
from pymel.core import datatypes
import json

import maya.OpenMaya as om

from mgear.core import applyop

#############################################
# CURVE
#############################################


def addCnsCurve(parent, name, centers, degree=1):
    """Create a curve attached to given centers. One point per center

    Arguments:
        parent (dagNode): Parent object.
        name (str): Name
        centers (list of dagNode): Object that will drive the curve.
        degree (int): 1 for linear curve, 3 for Cubic.

    Returns:
        dagNode: The newly created curve.
    """
    # rebuild list to avoid input list modification
    centers = centers[:]
    if degree == 3:
        if len(centers) == 2:
            centers.insert(0, centers[0])
            centers.append(centers[-1])
        elif len(centers) == 3:
            centers.append(centers[-1])

    points = [datatypes.Vector() for center in centers]

    node = addCurve(parent, name, points, False, degree)

    applyop.gear_curvecns_op(node, centers)

    return node


def addCurve(parent,
             name,
             points,
             close=False,
             degree=3,
             m=datatypes.Matrix()):
    """Create a NurbsCurve with a single subcurve.

    Arguments:
        parent (dagNode): Parent object.
        name (str): Name
        positions (list of float): points of the curve in a one dimension array
            [point0X, point0Y, point0Z, 1, point1X, point1Y, point1Z, 1, ...].
        close (bool): True to close the curve.
        degree (bool): 1 for linear curve, 3 for Cubic.
        m (matrix): Global transform.

    Returns:
        dagNode: The newly created curve.
    """
    if close:
        points.extend(points[:degree])
        knots = range(len(points) + degree - 1)
        node = pm.curve(n=name, d=degree, p=points, per=close, k=knots)
    else:
        node = pm.curve(n=name, d=degree, p=points)

    if m is not None:
        node.setTransformation(m)

    if parent is not None:
        parent.addChild(node)

    return node


def createCurveFromOrderedEdges(edgeLoop,
                                startVertex,
                                name,
                                parent=None,
                                degree=3):
    """Create a curve for a edgeloop ordering the list from starting vertex

    Arguments:
        edgeLoop (list ): List of edges
        startVertex (vertex): Starting vertex
        name (str): Name of the new curve.
        parent (dagNode): Parent of the new curve.
        degree (int): Degree of the new curve.

    Returns:
        dagNode: The newly created curve.
    """
    orderedEdges = []
    for e in edgeLoop:
        if startVertex in e.connectedVertices():
            orderedEdges.append(e)
            next = e
            break
    count = 0
    while True:
        for e in edgeLoop:
            if e in next.connectedEdges() and e not in orderedEdges:
                orderedEdges.append(e)
                next = e
                pass
        if len(orderedEdges) == len(edgeLoop):
            break
        count += 1
        if count > 100:
            break

    # return orderedEdges
    orderedVertex = [startVertex]
    orderedVertexPos = [startVertex.getPosition(space='world')]
    for e in orderedEdges:

        for v in e.connectedVertices():
            if v not in orderedVertex:
                orderedVertex.append(v)
                orderedVertexPos.append(v.getPosition(space='world'))

    crv = addCurve(parent, name, orderedVertexPos, degree=degree)
    return crv


def createCuveFromEdges(edgeList,
                        name,
                        parent=None,
                        degree=3,
                        sortingAxis="x"):
    """Create curve from a edge list.

    Arguments:
        edgeList (list): List of edges.
        name (str): Name of the new curve.
        parent (dagNode): Parent of the new curve.
        degree (int): Degree of the new curve.
        sortingAxis (str): Sorting axis x, y or z

    Returns:
        dagNode: The newly created curve.

    """
    if sortingAxis == "x":
        axis = 0
    elif sortingAxis == "y":
        axis = 1
    else:
        axis = 2

    vList = pm.polyListComponentConversion(edgeList, fe=True, tv=True)

    centers = []
    centersOrdered = []
    xOrder = []
    xReOrder = []
    for x in vList:
        vtx = pm.PyNode(x)
        for v in vtx:
            centers.append(v.getPosition(space='world'))
            # we use index [0] to order in X axis
            xOrder.append(v.getPosition(space='world')[axis])
            xReOrder.append(v.getPosition(space='world')[axis])
    for x in sorted(xReOrder):
        i = xOrder.index(x)
        centersOrdered.append(centers[i])

    crv = addCurve(parent, name, centersOrdered, degree=degree)
    return crv


def createCurveFromCurve(srcCrv, name, nbPoints, parent=None):
    """Create a curve from a curve

    Arguments:
        srcCrv (curve): The source curve.
        name (str): The new curve name.
        nbPoints (int): Number of control points for the new curve.
        parent (dagNode): Parent of the new curve.

    Returns:
        dagNode: The newly created curve.
    """
    if isinstance(srcCrv, str) or isinstance(srcCrv, unicode):
        srcCrv = pm.PyNode(srcCrv)
    length = srcCrv.length()
    parL = srcCrv.findParamFromLength(length)
    param = []
    increment = parL / (nbPoints - 1)
    p = 0.0
    for x in range(nbPoints):
        # we need to check that the param value never exceed the parL
        if p > parL:
            p = parL
        pos = srcCrv.getPointAtParam(p, space='world')
        param.append(pos)
        p += increment
    crv = addCurve(parent, name, param, close=False, degree=3)
    return crv


def getCurveParamAtPosition(crv, position):
    """Get curve parameter from a position

    Arguments:
        position (list of float): Represents the position in worldSpace
            exp: [1.4, 3.55, 42.6]
        crv (curve): The  source curve to get the parameter.

    Returns:
        list: paramenter and curve length
    """
    point = om.MPoint(position[0], position[1], position[2])

    dag = om.MDagPath()
    obj = om.MObject()
    oList = om.MSelectionList()
    oList.add(crv.name())
    oList.getDagPath(0, dag, obj)

    curveFn = om.MFnNurbsCurve(dag)
    length = curveFn.length()
    crv.findParamFromLength(length)

    paramUtill = om.MScriptUtil()
    paramPtr = paramUtill.asDoublePtr()

    point = curveFn.closestPoint(point, paramPtr, 0.001, om.MSpace.kObject)
    curveFn.getParamAtPoint(point, paramPtr, 0.001, om.MSpace.kObject)

    param = paramUtill.getDouble(paramPtr)

    return param, length


def findLenghtFromParam(crv, param):
    """
    Find lengtht from a curve parameter

    Arguments:
        param (float): The parameter to get the legth
        crv (curve): The source curve.

    Returns:
        float: Curve uLength

    Example:
        .. code-block:: python

            oParam, oLength = cur.getCurveParamAtPosition(upRope, cv)
            uLength = cur.findLenghtFromParam(upRope, oParam)
            u = uLength / oLength

    """
    node = pm.createNode("arcLengthDimension")
    pm.connectAttr(crv.getShape().attr("worldSpace[0]"),
                   node.attr("nurbsGeometry"))
    node.attr("uParamValue").set(param)
    uLength = node.attr("arcLength").get()
    pm.delete(node.getParent())
    return uLength


# ========================================

def get_color(node):
    """Get the color from shape node

    Args:
        node (TYPE): shape

    Returns:
        TYPE: Description
    """
    shp = node.getShape()
    if shp:
        if shp.overrideRGBColors.get():
            color = shp.overrideColorRGB.get()
        else:
            color = shp.overrideColor.get()

        return color


def set_color(node, color):
    """Set the color in the Icons.

    Arguments:
        node(dagNode): The object
        color (int or list of float): The color in index base or RGB.


    """
    # on Maya version.
    # version = mgear.core.getMayaver()

    if isinstance(color, int):

        for shp in node.listRelatives(shapes=True):
            shp.setAttr("overrideEnabled", True)
            shp.setAttr("overrideColor", color)
    else:
        for shp in node.listRelatives(shapes=True):
            shp.overrideEnabled.set(1)
            shp.overrideRGBColors.set(1)
            shp.overrideColorRGB.set(color[0], color[1], color[2])


# ========================================
# Curves IO ==============================
# ========================================

def collect_curve_shapes(crv, rplStr=["", ""]):
    """Collect curve shapes data

    Args:
        crv (dagNode): Curve object to collect the curve shapes data
        rplStr (list, optional): String to replace in names. This allow to
            change the curve names before store it.
            [old Name to replace, new name to set]

    Returns:
        dict, list: Curve shapes dictionary and curve shapes names
    """
    shapes_names = []
    shapesDict = {}
    for shape in crv.getShapes():
        shapes_names.append(shape.name().replace(rplStr[0], rplStr[1]))
        c_form = shape.form()
        degree = shape.degree()
        form = c_form.key
        form_id = c_form.index
        pnts = [[cv.x, cv.y, cv.z] for cv in shape.getCVs(space="object")]
        shapesDict[shape.name()] = {"points": pnts,
                                    "degree": degree,
                                    "form": form,
                                    "form_id": form_id}

    return shapesDict, shapes_names


def collect_selected_curve_data(objs=None):
    """Generate a dictionary descriving the curve data from selected objs

    Args:
        objs (None, optional): Optionally a list of object can be provided
    """
    if not objs:
        objs = pm.selected()

    return collect_curve_data(objs)


def collect_curve_data(objs, rplStr=["", ""]):
    """Generate a dictionary descriving the curve data

    Suport multiple objects

    Args:
        objs (dagNode): Curve object to store
        collect_trans (bool, optional): if false will skip the transformation
            matrix
        rplStr (list, optional): String to replace in names. This allow to
            change the curve names before store it.
            [old Name to replace, new name to set]

    Returns:
        dict: Curves data
    """

    # return if an empty list or None objects are pass
    if not objs:
        return

    if not isinstance(objs, list):
        objs = [objs]

    curves_dict = {}
    curves_dict["curves_names"] = []

    for x in objs:
        crv_name = x.name().replace(rplStr[0], rplStr[1])
        curves_dict["curves_names"].append(crv_name)
        if x.getParent():
            crv_parent = x.getParent().name().replace(rplStr[0], rplStr[1])
        else:
            crv_parent = None

        m = x.getMatrix(worldSpace=True)
        crv_transform = m.get()

        curveDict = {"shapes_names": [],
                     "crv_parent": crv_parent,
                     "crv_transform": crv_transform,
                     "crv_color": get_color(x)}

        shps, shps_n = collect_curve_shapes(x, rplStr)
        curveDict["shapes"] = shps
        curveDict["shapes_names"] = shps_n
        curves_dict[crv_name] = curveDict

    return curves_dict


def crv_parenting(data, crv, rplStr=["", ""], model=None):
    """Parent the new created curves

    Args:
        data (dict): serialized curve data
        crv (str): name of the curve to parent
        rplStr (list, optional): String to replace in names. This allow to
            change the curve names before store it.
            [old Name to replace, new name to set]
        model (dagNode, optional): Model top node to help find the correct
            parent, if  several objects with the same name
    """
    crv_dict = data[crv]
    crv_parent = crv_dict["crv_parent"]
    crv_p = None
    crv = crv.replace(rplStr[0], rplStr[1])
    parents = pm.ls(crv_parent)
    # this will try to find the correct parent by checking the top node
    # in situations where the name is reapet in many places under same
    # hierarchy this method will fail.
    if len(parents) > 1 and model:
        for p in parents:
            if model.name() in p.name():
                crv_p = p
                break
    elif len(parents) == 1:
        crv_p = parents[0]
    else:
        pm.displayWarning("More than one parent with the same name found for"
                          " {}, or not top model root provided.".format(crv))
        pm.displayWarning("This curve"
                          "  can't be parented. Please do it manually or"
                          " review the scene")
    if crv_p:
        # we need to ensure that we parent is the new curve.
        crvs = pm.ls(crv)
        if len(crvs) > 1:
            for c in crvs:
                if not c.getParent():  # if not parent means is the new
                    crv = c
                    break
        elif len(crvs) == 1:
            crv = crvs[0]
        pm.parent(crv,
                  crv_p)


def create_curve_from_data_by_name(crv,
                                   data,
                                   replaceShape=False,
                                   rebuildHierarchy=False,
                                   rplStr=["", ""],
                                   model=None):
    """Build one curve from a given curve data dict

    Args:
        crv (str): name of the crv to create
        data (dict): serialized curve data
        replaceShape (bool, optional): If True, will replace the shape on
            existing objects
        rebuildHierarchy (bool, optional): If True, will regenerate the
            hierarchy
        rplStr (list, optional): String to replace in names. This allow to
            change the curve names before store it.
            [old Name to replace, new name to set]
        model (dagNode, optional): Model top node to help find the correct
            parent, if  several objects with the same name
    """
    crv_dict = data[crv]

    crv_transform = crv_dict["crv_transform"]
    shp_dict = crv_dict["shapes"]
    color = crv_dict["crv_color"]
    if replaceShape:
        first_shape = pm.ls(crv.replace(rplStr[0], rplStr[1]))
        if first_shape and model and model == first_shape[0].getParent(-1):
            pass
        else:
            first_shape = None
    else:
        first_shape = None

    if first_shape:
        first_shape = first_shape[0]
        # clean old shapes
        pm.delete(first_shape.listRelatives(shapes=True))
    for sh in crv_dict["shapes_names"]:
        points = shp_dict[sh]["points"]
        form = shp_dict[sh]["form"]
        degree = shp_dict[sh]["degree"]
        knots = range(len(points) + degree - 1)
        if form != "open":
            close = True
        else:
            close = False

        # we dont use replace in order to support multiple shapes
        nsh = crv.replace(rplStr[0], rplStr[1])
        obj = pm.curve(name=nsh.replace("Shape", ""),
                       point=points,
                       periodic=close,
                       degree=degree,
                       knot=knots)
        set_color(obj, color)
        # handle multiple shapes in the same transform
        if not first_shape:
            first_shape = obj
            first_shape.setTransformation(crv_transform)
        else:
            for extra_shp in obj.listRelatives(shapes=True):
                first_shape.addChild(extra_shp, add=True, shape=True)
                pm.delete(obj)

    if rebuildHierarchy:
        crv_parenting(data, crv, rplStr, model)


def create_curve_from_data(data,
                           replaceShape=False,
                           rebuildHierarchy=False,
                           rplStr=["", ""],
                           model=None):
    """Build the curves from a given curve data dict

    Hierarchy rebuild after all curves are build to avoid lost parents

    Args:
        data (dict): serialized curve data
        replaceShape (bool, optional): If True, will replace the shape on
            existing objects
        rebuildHierarchy (bool, optional): If True, will regenerate the
            hierarchy
    """

    for crv in data["curves_names"]:
        create_curve_from_data_by_name(crv,
                                       data,
                                       replaceShape,
                                       rebuildHierarchy=False,
                                       rplStr=rplStr)

    # parenting
    if rebuildHierarchy:
        for crv in data["curves_names"]:
            crv_parenting(data, crv, rplStr, model)


def update_curve_from_data(data, rplStr=["", ""]):
    """update the curves from a given curve data dict

    Args:
        data (dict): serialized curve data
    """

    for crv in data["curves_names"]:
        crv_dict = data[crv]

        shp_dict = crv_dict["shapes"]
        color = crv_dict["crv_color"]
        first_shape = pm.ls(crv.replace(rplStr[0], rplStr[1]))
        if not first_shape:
            pm.displayWarning("Couldn't find: {}. Shape will be "
                              "skipped, since there is nothing to "
                              "replace".format(crv.replace(rplStr[0],
                                                           rplStr[1])))
            continue

        if first_shape:
            first_shape = first_shape[0]
            # Because we don know if the number of shapes will match between
            # the old and new shapes. We only take care of the connections
            # of the first shape. Later will be apply to all the new shapes

            # store shapes connections
            shapes = first_shape.listRelatives(shapes=True)
            if shapes:
                cnx = shapes[0].listConnections(plugs=True, c=True)
                cnx = [[c[1], c[0].shortName()] for c in cnx]
                # Disconnect the conexion before delete the old shapes
                for s in shapes:
                    for c in s.listConnections(plugs=True, c=True):
                        pm.disconnectAttr(c[0])
                # clean old shapes
                pm.delete(shapes)

        for sh in crv_dict["shapes_names"]:
            points = shp_dict[sh]["points"]
            form = shp_dict[sh]["form"]
            degree = shp_dict[sh]["degree"]
            knots = range(len(points) + degree - 1)
            if form != "open":
                close = True
            else:
                close = False
            # we dont use replace in order to support multiple shapes
            obj = pm.curve(replace=False,
                           name=sh.replace(rplStr[0], rplStr[1]),
                           point=points,
                           periodic=close,
                           degree=degree,
                           knot=knots)
            set_color(obj, color)
            for extra_shp in obj.listRelatives(shapes=True):
                # Restore shapes connections
                for c in cnx:
                    pm.connectAttr(c[0], extra_shp.attr(c[1]))
                first_shape.addChild(extra_shp, add=True, shape=True)
                pm.delete(obj)

        # clean up shapes names
        for sh in first_shape.getShapes():
            pm.rename(sh, sh.name().replace("ShapeShape", "Shape"))


def export_curve(filePath=None, objs=None):
    """Export the curve data to a json file

    Args:
        filePath (None, optional): Description
        objs (None, optional): Description

    Returns:
        TYPE: Description
    """

    if not filePath:
        startDir = pm.workspace(q=True, rootDirectory=True)
        filePath = pm.fileDialog2(
            dialogStyle=2,
            fileMode=0,
            startingDirectory=startDir,
            fileFilter='NURBS Curves .crv (*%s)' % ".crv")
        if not filePath:
            pm.displayWarning("Invalid file path")
            return
        if not isinstance(filePath, basestring):
            filePath = filePath[0]

    data = collect_selected_curve_data(objs)
    data_string = json.dumps(data, indent=4, sort_keys=True)
    f = open(filePath, 'w')
    f.write(data_string)
    f.close()


def _curve_from_file(filePath=None):
    if not filePath:
        startDir = pm.workspace(q=True, rootDirectory=True)
        filePath = pm.fileDialog2(
            dialogStyle=2,
            fileMode=1,
            startingDirectory=startDir,
            fileFilter='NURBS Curves .crv (*%s)' % ".crv")

    if not filePath:
        pm.displayWarning("Invalid file path")
        return
    if not isinstance(filePath, basestring):
        filePath = filePath[0]
    configDict = json.load(open(filePath))

    return configDict


def import_curve(filePath=None,
                 replaceShape=False,
                 rebuildHierarchy=False,
                 rplStr=["", ""]):
    create_curve_from_data(_curve_from_file(filePath),
                           replaceShape,
                           rebuildHierarchy,
                           rplStr)


def update_curve_from_file(filePath=None, rplStr=["", ""]):
    # update a curve data from json file
    update_curve_from_data(_curve_from_file(filePath), rplStr)
