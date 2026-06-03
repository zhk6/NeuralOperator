import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import viennaps as ps

# print("succeed import viennaps")

# from utils.vtp_processor import vtp_processor



# 兼容相对导入和绝对导入
try:
    from .DEFAULTS import DEFAULTS
except ImportError:
    from DEFAULTS import DEFAULTS

def holeEtching(
    *,
    D: int = int(DEFAULTS["D"]),
    lengthUnit: str = DEFAULTS["lengthUnit"],
    gridDelta: float = float(DEFAULTS["gridDelta"]),
    xExtent: float = float(DEFAULTS["xExtent"]),
    yExtent: float = float(DEFAULTS["yExtent"]),
    holeRadius: float = float(DEFAULTS["holeRadius"]),
    maskHeight: float = float(DEFAULTS["maskHeight"]),
    taperAngle: float = float(DEFAULTS["taperAngle"]),
    processTime: float = float(DEFAULTS["processTime"]),
    timeUnit: str = DEFAULTS["timeUnit"],
    ionFlux: float = float(DEFAULTS["ionFlux"]),
    etchantFlux: float = float(DEFAULTS["etchantFlux"]),
    oxygenFlux: float = float(DEFAULTS["oxygenFlux"]),
    ionExponent: float = float(DEFAULTS["ionExponent"]),
    meanEnergy: float = float(DEFAULTS["meanEnergy"]),
    sigmaEnergy: float = float(DEFAULTS["sigmaEnergy"]),
    A_O: float = float(DEFAULTS["A_O"]),
    A_Si: float = float(DEFAULTS["A_Si"]),
    etchStopDepth: float = float(DEFAULTS["etchStopDepth"]),
    integrationScheme: str = DEFAULTS["integrationScheme"],
    raysPerPoint: int = int(DEFAULTS["raysPerPoint"]),
    vtpFile: str = DEFAULTS["vtpFile"],
    txtFile: str = DEFAULTS["txtFile"],
    logLevel: str = DEFAULTS["logLevel"],
    saveFile: bool = True,
):
    # 用于运行仿真程序的函数，未给定的参数将使用DEFAULTS中的默认值
    params = {
        "D": D,
        "lengthUnit": lengthUnit,
        "gridDelta": gridDelta,
        "xExtent": xExtent,
        "yExtent": yExtent,
        "holeRadius": holeRadius,
        "maskHeight": maskHeight,
        "taperAngle": taperAngle,
        "processTime": processTime,
        "timeUnit": timeUnit,
        "ionFlux": ionFlux,
        "etchantFlux": etchantFlux,
        "oxygenFlux": oxygenFlux,
        "ionExponent": ionExponent,
        "meanEnergy": meanEnergy,
        "sigmaEnergy": sigmaEnergy,
        "A_O": A_O,
        "A_Si": A_Si,
        "etchStopDepth": etchStopDepth,
        "integrationScheme": integrationScheme,
        "raysPerPoint": raysPerPoint,
        "vtpFile": vtpFile,
        "txtFile": txtFile,
        "logLevel": logLevel,
    }

    # switch between 2D and 3D mode
    ps.setDimension(params["D"])

    # params = ps.readConfigFile(args.filename)

    # print intermediate output surfaces during the process
    ps.Logger.setLogLevel(eval(f"ps.LogLevel.{params['logLevel']}"))

    ps.Length.setUnit(params["lengthUnit"])
    ps.Time.setUnit(params["timeUnit"])

    # geometry setup, all units in um
    geometry = ps.Domain(
        gridDelta=params["gridDelta"],
        xExtent=params["xExtent"],
        yExtent=params["yExtent"],
    )
    ps.MakeHole(
        domain=geometry,
        holeRadius=params["holeRadius"],
        holeDepth=0.0,
        maskHeight=params["maskHeight"],
        maskTaperAngle=params["taperAngle"],
        holeShape=ps.HoleShape.HALF,
    ).apply()

    # use pre-defined model SF6O2 etching model
    modelParams = ps.SF6O2Etching.defaultParameters()
    modelParams.ionFlux = params["ionFlux"]
    modelParams.etchantFlux = params["etchantFlux"]
    modelParams.passivationFlux = params["oxygenFlux"]
    modelParams.Ions.meanEnergy = params["meanEnergy"]
    modelParams.Ions.sigmaEnergy = params["sigmaEnergy"]
    modelParams.Ions.exponent = params["ionExponent"]
    modelParams.Passivation.A_ie = params["A_O"]
    modelParams.Substrate.A_ie = params["A_Si"]
    modelParams.etchStopDepth = params["etchStopDepth"]
    model = ps.SF6O2Etching(modelParams)

    covParams = ps.CoverageParameters()
    covParams.tolerance = 1e-4

    rayParams = ps.RayTracingParameters()
    rayParams.raysPerPoint = int(params["raysPerPoint"])
    rayParams.smoothingNeighbors = 2

    advParams = ps.AdvectionParameters()
    advParams.integrationScheme = ps.util.convertIntegrationScheme(
        params["integrationScheme"]
    )

    # process setup
    process = ps.Process(geometry, model)
    process.setProcessDuration(params["processTime"])  # seconds
    process.setParameters(covParams)
    process.setParameters(rayParams)
    process.setParameters(advParams)

    # print initial surface
    # if saveFile:
    #     geometry.saveSurfaceMesh(filename="initial.vtp")

    # run the process
    process.apply()

    # domainEval = geometry.getLevelSets()[-1]

    # print final surface
    if saveFile:
        geometry.saveVolumeMesh(filename=params["vtpFile"], addInterfaces=False)
        # _vtp_processor = vtp_processor()
        # _vtp_processor.vtp2txt(filename=params["vtpFile"], txt_name=params["txtFile"])
    
    # print(geometry)
    # try:
    mesh = geometry.getSurfaceMesh(addInterfaces=False)
    # except TypeError:
    #     mesh = geometry.getSurfaceMesh()
    
    
    nodes = mesh.getNodes()
    # print(nodes)
    return nodes

if __name__ == "__main__":
    holeEtching()