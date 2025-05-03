from typing import List, Optional

from pydantic import BaseModel, Field


class PVGISGridConnectedTrackingPVSystemsRequest(BaseModel):
    lat: float = Field(..., description="Latitude, in decimal degrees, south is negative.")
    lon: float = Field(..., description="Longitude, in decimal degrees, west is negative.")
    usehorizon: Optional[int] = Field(1, description="Use horizon (1 = yes, 0 = no). Default is 1.")
    userhorizon: Optional[List[float]] = Field(
        None, description="List of horizon heights at equidistant directions (degrees)."
    )
    raddatabase: Optional[str] = Field(
        None,
        description='Radiation database name. Options: "PVGIS-SARAH", "PVGIS-NSRDB", "PVGIS-ERA5", "PVGIS-COSMO", "PVGIS-CMSAF".',
    )
    peakpower: float = Field(..., description="Nominal power of the PV system, in kW.")
    pvtechchoice: Optional[str] = Field(
        "crystSi",
        description='PV technology. Choices: "crystSi", "CIS", "CdTe", "Unknown".',
    )
    mountingplace: Optional[str] = Field(
        "free",
        description='Type of mounting: "free" (free-standing), "building" (building-integrated).',
    )
    loss: float = Field(..., description="Sum of system losses, in percent.")
    fixed: Optional[int] = Field(1, description="Fixed mounted system (1 = yes, 0 = no). Default is 1.")
    angle: Optional[float] = Field(0, description="Inclination angle from the horizontal plane (degrees).")
    aspect: Optional[float] = Field(
        0,
        description="Orientation (azimuth) angle of the system (0=south, 90=west, -90=east).",
    )
    optimalinclination: Optional[int] = Field(0, description="Calculate optimal inclination angle (1 = yes, 0 = no).")
    optimalangles: Optional[int] = Field(
        0,
        description="Calculate optimal inclination and orientation angles (1 = yes, 0 = no).",
    )
    inclined_axis: Optional[int] = Field(0, description="Calculate a single inclined axis system (1 = yes, 0 = no).")
    inclined_optimum: Optional[int] = Field(
        0,
        description="Calculate optimum angle for a single inclined axis system (1 = yes, 0 = no).",
    )
    inclinedaxisangle: Optional[float] = Field(0, description="Inclination angle for a single inclined axis system.")
    vertical_axis: Optional[int] = Field(0, description="Calculate a single vertical axis system (1 = yes, 0 = no).")
    vertical_optimum: Optional[int] = Field(
        0,
        description="Calculate optimum angle for a single vertical axis system (1 = yes, 0 = no).",
    )
    verticalaxisangle: Optional[float] = Field(0, description="Inclination angle for a single vertical axis system.")
    twoaxis: Optional[int] = Field(0, description="Calculate a two-axis tracking system (1 = yes, 0 = no).")
    pvprice: Optional[int] = Field(0, description="Calculate PV electricity price (1 = yes, 0 = no).")
    systemcost: Optional[float] = Field(None, description="Total cost of installing the PV system (if pvprice=1).")
    interest: Optional[float] = Field(None, description="Interest rate in % per year (if pvprice=1).")
    lifetime: Optional[int] = Field(25, description="Expected lifetime of the PV system in years.")
    outputformat: Optional[str] = Field("csv", description='Output format: "csv", "basic", or "json".')
    browser: Optional[int] = Field(
        0,
        frozen=True,
        description="Use 1 if accessing from a web browser and want to save the data.",
    )


class PVGISOffGridRequest(BaseModel):
    lat: float = Field(..., description="Latitude, in decimal degrees, south is negative.")
    lon: float = Field(..., description="Longitude, in decimal degrees, west is negative.")
    usehorizon: Optional[int] = Field(
        1,
        description="Calculate taking into account shadows from high horizon (1 = yes, 0 = no). Default is 1.",
    )
    userhorizon: Optional[List[float]] = Field(
        None, description="List of horizon heights at equidistant directions (degrees)."
    )
    raddatabase: Optional[str] = Field(
        None,
        description='Radiation database name. Options: "PVGIS-SARAH", "PVGIS-NSRDB", "PVGIS-ERA5", "PVGIS-COSMO", "PVGIS-CMSAF".',
    )
    peakpower: float = Field(..., description="Nominal power of the PV system, in W.")
    angle: Optional[float] = Field(
        0,
        description="Inclination angle from horizontal plane of the (fixed) PV system.",
    )
    aspect: Optional[float] = Field(
        0,
        description="Orientation (azimuth) angle of the system (0=south, 90=west, -90=east).",
    )
    batterysize: float = Field(..., description="Battery size (energy capacity) in watt-hours (Wh).")
    cutoff: float = Field(
        ...,
        description="Batteries cutoff in %. The charge cannot go below this percentage.",
    )
    consumptionday: float = Field(..., description="Daily energy consumption of the system in watt-hours (Wh).")
    hourconsumption: Optional[List[float]] = Field(
        None,
        description="List of 24 values representing the hourly consumption fraction. The sum must equal 1.",
    )
    outputformat: Optional[str] = Field("csv", description='Output format: "csv", "basic", or "json".')
    browser: Optional[int] = Field(
        0,
        frozen=True,
        description="Use 1 if accessing from a web browser and want to save the data.",
    )


class PVGISMonthlyRadiationRequest(BaseModel):
    lat: float = Field(..., description="Latitude in decimal degrees. South is negative.")
    lon: float = Field(..., description="Longitude in decimal degrees. West is negative.")
    usehorizon: Optional[int] = Field(
        1,
        description="Take high horizon shadows into account (1 = yes, 0 = no). Default is 1.",
    )
    userhorizon: Optional[List[float]] = Field(
        None, description="List of horizon heights at equidistant directions (degrees)."
    )
    raddatabase: Optional[str] = Field(
        None,
        description="Radiation database. Options: 'PVGIS-SARAH', 'PVGIS-NSRDB', 'PVGIS-ERA5', 'PVGIS-COSMO', 'PVGIS-CMSAF'.",
    )
    startyear: Optional[int] = Field(None, description="First year for monthly averages output.")
    endyear: Optional[int] = Field(None, description="Final year for monthly averages output.")
    horirrad: Optional[int] = Field(
        0,
        description="Output horizontal plane irradiation (1 = yes, 0 = no). Default is 0.",
    )
    optrad: Optional[int] = Field(
        0,
        description="Output annual optimal angle plane irradiation (1 = yes, 0 = no). Default is 0.",
    )
    selectrad: Optional[int] = Field(
        0,
        description="Output irradiation on plane of selected inclination (1 = yes, 0 = no). Default is 0.",
    )
    angle: Optional[float] = Field(
        0,
        description="Inclination angle for the selected inclination irradiation option.",
    )
    mr_dni: Optional[int] = Field(
        0,
        description="Output direct normal irradiation (1 = yes, 0 = no). Default is 0.",
    )
    d2g: Optional[int] = Field(
        0,
        description="Output monthly ratio of diffuse to global radiation (1 = yes, 0 = no). Default is 0.",
    )
    avtemp: Optional[int] = Field(
        0,
        description="Output monthly average daily temperature (1 = yes, 0 = no). Default is 0.",
    )
    outputformat: Optional[str] = Field(
        "csv",
        description="Output format. Choices: 'csv', 'basic', or 'json'. Default is 'csv'.",
    )
    browser: Optional[int] = Field(
        0,
        frozen=True,
        description="Use 1 to save the data to a file when accessing from a web browser.",
    )


class PVGISDailyRadiationRequest(BaseModel):
    lat: float = Field(..., description="Latitude in decimal degrees. South is negative.")
    lon: float = Field(..., description="Longitude in decimal degrees. West is negative.")
    usehorizon: Optional[int] = Field(
        1,
        description="Take high horizon shadows into account (1 = yes, 0 = no). Default is 1.",
    )
    userhorizon: Optional[List[float]] = Field(
        None, description="List of horizon heights at equidistant directions (degrees)."
    )
    raddatabase: Optional[str] = Field(
        None,
        description="Radiation database. Options: 'PVGIS-SARAH', 'PVGIS-NSRDB', 'PVGIS-ERA5', 'PVGIS-COSMO', 'PVGIS-CMSAF'.",
    )
    month: int = Field(
        ...,
        description="Number of the month (1 for January, 12 for December, 0 for all months).",
    )
    angle: Optional[float] = Field(
        0,
        description="Inclination angle from horizontal plane of the (fixed) PV system.",
    )
    aspect: Optional[float] = Field(
        0,
        description="Orientation (azimuth) angle of the system (0=south, 90=west, -90=east).",
    )
    global_: Optional[int] = Field(
        0,
        alias="global",
        description="Output global, direct, and diffuse in-plane irradiances (1 = yes, 0 = no).",
    )
    glob_2axis: Optional[int] = Field(
        0,
        description="Output global, direct, and diffuse two-axis tracking irradiances (1 = yes, 0 = no).",
    )
    clearsky: Optional[int] = Field(0, description="Output global clear-sky irradiance (1 = yes, 0 = no).")
    clearsky_2axis: Optional[int] = Field(
        0,
        description="Output global clear-sky two-axis tracking irradiance (1 = yes, 0 = no).",
    )
    showtemperatures: Optional[int] = Field(0, description="Output daily temperature profile (1 = yes, 0 = no).")
    localtime: Optional[int] = Field(
        0,
        description="Output time in local time zone instead of UTC (1 = yes, 0 = no).",
    )
    outputformat: Optional[str] = Field(
        "csv",
        description="Output format. Choices: 'csv', 'basic', or 'json'. Default is 'csv'.",
    )
    browser: Optional[int] = Field(
        0,
        frozen=True,
        description="Use 1 if accessing from a web browser and want to save the data.",
    )


class PVGISHourlyRadiationRequest(BaseModel):
    lat: float = Field(..., description="Latitude in decimal degrees. South is negative.")
    lon: float = Field(..., description="Longitude in decimal degrees. West is negative.")
    usehorizon: Optional[int] = Field(
        1,
        description="Take high horizon shadows into account (1 = yes, 0 = no). Default is 1.",
    )
    userhorizon: Optional[List[float]] = Field(
        None, description="List of horizon heights at equidistant directions (degrees)."
    )
    raddatabase: Optional[str] = Field(
        None,
        description="Radiation database. Options: 'PVGIS-SARAH', 'PVGIS-NSRDB', 'PVGIS-ERA5', 'PVGIS-COSMO', 'PVGIS-CMSAF'.",
    )
    startyear: Optional[int] = Field(None, description="First year for hourly averages output.")
    endyear: Optional[int] = Field(None, description="Final year for hourly averages output.")
    pvcalculation: Optional[int] = Field(
        0,
        description="Include hourly PV production estimation (1 = yes, 0 = no). Default is 0.",
    )
    peakpower: Optional[float] = Field(
        None,
        description="Nominal power of the PV system (kW). Required if pvcalculation = 1.",
    )
    pvtechchoice: Optional[str] = Field(
        "crystSi",
        description="PV technology type. Choices: 'crystSi', 'CIS', 'CdTe', 'Unknown'.",
    )
    mountingplace: Optional[str] = Field(
        "free",
        description="Mounting type: 'free' (free-standing) or 'building' (building-integrated). Default is 'free'.",
    )
    loss: Optional[float] = Field(None, description="System losses percentage. Required if pvcalculation = 1.")
    trackingtype: Optional[int] = Field(
        0,
        description="Type of sun-tracking used (0 = fixed, 1 = horizontal N-S, 2 = two-axis, 3 = vertical, 4 = horizontal E-W, 5 = inclined N-S).",
    )
    angle: Optional[float] = Field(
        0,
        description="Inclination angle from horizontal plane (not relevant for 2-axis tracking).",
    )
    aspect: Optional[float] = Field(
        0,
        description="Orientation (azimuth) angle (0=south, 90=west, -90=east, not relevant for tracking).",
    )
    optimalinclination: Optional[int] = Field(
        0,
        description="Calculate optimum inclination angle (1 = yes, 0 = no). Not relevant for 2-axis tracking.",
    )
    optimalangles: Optional[int] = Field(
        0,
        description="Calculate optimum inclination AND orientation angles (1 = yes, 0 = no). Not relevant for tracking.",
    )
    components: Optional[int] = Field(
        0,
        description="Output beam, diffuse, and reflected radiation components (1 = yes, 0 = no). Default is 0.",
    )
    outputformat: Optional[str] = Field(
        "csv",
        description="Output format. Choices: 'csv', 'basic', 'json'. Default is 'csv'.",
    )
    browser: Optional[int] = Field(
        0,
        frozen=True,
        description="Use 1 to save the data when accessing from a web browser.",
    )


class PVGISTMYRequest(BaseModel):
    lat: float = Field(..., description="Latitude in decimal degrees. South is negative.")
    lon: float = Field(..., description="Longitude in decimal degrees. West is negative.")
    usehorizon: Optional[int] = Field(
        1,
        description="Take high horizon shadows into account (1 = yes, 0 = no). Default is 1.",
    )
    userhorizon: Optional[List[float]] = Field(
        None, description="List of horizon heights at equidistant directions (degrees)."
    )
    startyear: Optional[int] = Field(None, description="First year of the TMY period.")
    endyear: Optional[int] = Field(
        None,
        description="Final year of the TMY period. Must be at least 10 years after startyear.",
    )
    outputformat: Optional[str] = Field(
        "csv",
        description="Output format. Choices: 'csv', 'basic', 'epw' (EnergyPlus format), or 'json'. Default is 'csv'.",
    )
    browser: Optional[int] = Field(
        0,
        frozen=True,
        description="Use 1 to save the data when accessing from a web browser.",
    )
