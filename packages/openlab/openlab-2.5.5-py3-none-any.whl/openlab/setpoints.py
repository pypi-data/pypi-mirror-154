def all_setpoints():
    """
    DEPRECATED
    Returns a list of all available/possible setpoints
    Subject to change in the future
    """
    empty_setpoints = [
        "ChokeOpening", "FlowRateIn", "TopOfStringVelocity",
        "DesiredROP", "SurfaceRPM", "ChokePumpFlowRateIn", "BopChokeOpening",
        "MainPitActive", "MainPitReturn", "ControlActivePit",
        "ControlActivePitDensity", "ControlActivePitTemperature",
        "WOBAutoDriller", "DesiredWOB", "WOBProportionalGain",
        "WOBIntegralGain"
    ]
    return empty_setpoints

valid_tags = [
        "ChokeOpening", "FlowRateIn", "TopOfStringVelocity",
        "DesiredROP", "SurfaceRPM", "ChokePumpFlowRateIn", "BopChokeOpening",
        "MainPitActive", "MainPitReturn", "ControlActivePit",
        "ControlActivePitDensity", "ControlActivePitTemperature",
        "WOBAutoDriller", "DesiredWOB", "WOBProportionalGain",
        "WOBIntegralGain"
    ]

class Setpoints():
    """
    A class property for the setpoints
    """
    def __init__(self):
        self.ChokeOpening = 1 # 0=closed 1=Open
        self.FlowRateIn = None
        self.TopOfStringVelocity = None
        self.DesiredROP  = None
        self.SurfaceRPM = None
        self.ChokePumpFlowRateIn = None
        self.BopChokeOpening = 1 # 0=closed 1=Open
        self.MainPitActive = None # bool
        self.MainPitReturn = None # bool
        self.ControlActivePit = None #bool
        self.ControlActivePitDensity = None # float
        self.ControlActivePitTemperature = None # float
        self.WOBAutoDriller = None # bool
        self.DesiredWOB = None # float
        self.WOBProportionalGain = None # float
        self.WOBIntegralGain = None # float
    
    @property
    def ChokeOpening(self): return self.__ChokeOpening
    @ChokeOpening.setter
    def ChokeOpening(self, value): self.__ChokeOpening = value

    @property
    def FlowRateIn(self): return self.__FlowRateIn
    @FlowRateIn.setter
    def FlowRateIn(self, value): self.__FlowRateIn = value

    @property
    def TopOfStringVelocity(self): return self.__TopOfStringVelocity
    @TopOfStringVelocity.setter
    def TopOfStringVelocity(self, value): self.__TopOfStringVelocity = value

    @property
    def DesiredROP(self): return self.__DesiredROP
    @DesiredROP.setter
    def DesiredROP(self, value): self.__DesiredROP = value            

    @property
    def SurfaceRPM(self): return self.__SurfaceRPM
    @SurfaceRPM.setter
    def SurfaceRPM(self, value): self.__SurfaceRPM = value

    @property
    def ChokePumpFlowRateIn(self): return self.__ChokePumpFlowRateIn
    @ChokePumpFlowRateIn.setter
    def ChokePumpFlowRateIn(self, value): self.__ChokePumpFlowRateIn = value

    @property
    def BopChokeOpening(self): return self.__BopChokeOpening
    @BopChokeOpening.setter
    def BopChokeOpening(self, value): self.__BopChokeOpening = value

    @property
    def MainPitActive(self): return self.__MainPitActive
    @MainPitActive.setter
    def MainPitActive(self, value): self.__MainPitActive = value

    @property
    def MainPitReturn(self): return self.__MainPitReturn
    @MainPitReturn.setter
    def MainPitReturn(self, value): self.__MainPitReturn = value

    @property
    def ControlActivePit(self): return self.__ControlActivePit
    @ControlActivePit.setter
    def ControlActivePit(self, value): self.__ControlActivePit = value

    @property
    def ControlActivePitDensity(self): return self.__ControlActivePitDensity
    @ControlActivePitDensity.setter
    def ControlActivePitDensity(self, value): self.__ControlActivePitDensity = value

    @property
    def ControlActivePitTemperature(self): return self.__ControlActivePitTemperature
    @ControlActivePitTemperature.setter
    def ControlActivePitTemperature(self, value): self.__ControlActivePitTemperature = value

    @property
    def WOBAutoDriller(self): return self.__WOBAutoDriller
    @WOBAutoDriller.setter
    def WOBAutoDriller(self, value): self.__WOBAutoDriller = value

    @property
    def DesiredWOB(self): return self.__DesiredWOB
    @DesiredWOB.setter
    def DesiredWOB(self, value): self.__DesiredWOB = value

    @property
    def WOBProportionalGain(self): return self.__WOBProportionalGain
    @WOBProportionalGain.setter
    def WOBProportionalGain(self, value): self.__WOBProportionalGain = value

    @property
    def WOBIntegralGain(self): return self.__WOBIntegralGain
    @WOBIntegralGain.setter
    def WOBIntegralGain(self, value): self.__WOBIntegralGain = value
