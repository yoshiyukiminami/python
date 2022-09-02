class FieldProperty:

    def __init__(self):
        self._measurement_method = None
        self._measurement_date = None
        self._mining_soil_method = None
        self._mining_soil_day = None
        self._class_clops = None
        self._clops = None
        self._shipping_organization = None
        self._company = None
        self._name = None

    @property
    def shipping_organization(self) -> str:
        return self._shipping_organization

    @shipping_organization.setter
    def shipping_organization(self, value: str):
        self._shipping_organization = value

    @property
    def company(self) -> str:
        return self._company

    @company.setter
    def company(self, value: str):
        self._company = value

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = value

    @property
    def clops(self) -> str:
        return self._clops

    @clops.setter
    def clops(self, value: str):
        self._clops = value

    @property
    def class_clops(self) -> str:
        return self._class_clops

    @class_clops.setter
    def class_clops(self, value: str):
        self._class_clops = value

    @property
    def mining_soil_day(self) -> str:
        return self._mining_soil_day

    @mining_soil_day.setter
    def mining_soil_day(self, value: str):
        self._mining_soil_day = value

    @property
    def mining_soil_method(self) -> str:
        return self._mining_soil_method

    @mining_soil_method.setter
    def mining_soil_method(self, value: str):
        self._mining_soil_method = value

    @property
    def measurement_date(self) -> str:
        return self._measurement_date

    @measurement_date.setter
    def measurement_date(self, value: str):
        self._measurement_date = value

    @property
    def measurement_method(self) -> str:
        return self._measurement_method

    @measurement_method.setter
    def measurement_method(self, value: str):
        self._measurement_method = value

    def formatted_text(self):
        return f"出荷団体：{self.shipping_organization}　生産者：{self.company}\n圃場名：{self.name}　作物：{self.clops}　作型：{self.class_clops}採土日：{self.mining_soil_day}\n採土方法：{self.mining_soil_method}\n土壌硬度測定日： {self.measurement_date}\n測定方法：{self.measurement_method}"
