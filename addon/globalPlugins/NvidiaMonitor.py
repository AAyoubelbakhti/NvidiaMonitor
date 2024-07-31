import os
import sys
import addonHandler
import globalPluginHandler
import scriptHandler
import ui

addonHandler.initTranslation()

# Agregar el directorio del complemento y el directorio 'lib' al PATH
dirAddon = os.path.dirname(__file__)
sys.path.append(dirAddon)
sys.path.append(os.path.join(dirAddon, "lib"))

import pynvml

# Eliminar los directorios añadidos al PATH para evitar conflictos
del sys.path[-2:]

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
    def __init__(self):
        super(GlobalPlugin, self).__init__()
        try:
            pynvml.nvmlInit()
        except pynvml.NVMLError as e:
            ui.message(f"Error inicializando NVML: {str(e)}")

    def terminate(self):
        try:
            pynvml.nvmlShutdown()
        except pynvml.NVMLError as e:
            ui.message(f"Error apagando NVML: {str(e)}")
        super(GlobalPlugin, self).terminate()

    @scriptHandler.script(
        description="Anuncia el nombre de la GPU",
        gesture="kb:NVDA+shift+g"
    )
    def script_sayGPUName(self, gesture):
        try:
            handle = pynvml.nvmlDeviceGetHandleByIndex(0)
            gpu_name = pynvml.nvmlDeviceGetName(handle)
            ui.message(f"Nombre de la GPU: {gpu_name}")
        except pynvml.NVMLError as e:
            ui.message(f"Error obteniendo el nombre de la GPU: {str(e)}")

    @scriptHandler.script(
        description="Anuncia la utilización de la GPU",
        gesture="kb:NVDA+shift+u"
    )
    def script_sayGPUUtilization(self, gesture):
        try:
            handle = pynvml.nvmlDeviceGetHandleByIndex(0)
            utilization = pynvml.nvmlDeviceGetUtilizationRates(handle)
            ui.message(f"Utilización de la GPU: {utilization.gpu}%")
        except pynvml.NVMLError as e:
            ui.message(f"Error obteniendo la utilización de la GPU: {str(e)}")

    @scriptHandler.script(
        description="Anuncia la memoria de la GPU",
        gesture="kb:NVDA+shift+m"
    )
    def script_sayGPUMemory(self, gesture):
        try:
            handle = pynvml.nvmlDeviceGetHandleByIndex(0)
            memory_info = pynvml.nvmlDeviceGetMemoryInfo(handle)
            free_memory = memory_info.free // 1024**2
            used_memory = memory_info.used // 1024**2
            total_memory = memory_info.total // 1024**2
            ui.message(f"Memoria de la GPU - Libre: {free_memory} MB, Usada: {used_memory} MB, Total: {total_memory} MB")
        except pynvml.NVMLError as e:
            ui.message(f"Error obteniendo la memoria de la GPU: {str(e)}")

    @scriptHandler.script(
        description="Anuncia la temperatura de la GPU",
        gesture="kb:NVDA+shift+t"
    )
    def script_sayGPUTemperature(self, gesture):
        try:
            handle = pynvml.nvmlDeviceGetHandleByIndex(0)
            temperature = pynvml.nvmlDeviceGetTemperature(handle, pynvml.NVML_TEMPERATURE_GPU)
            ui.message(f"Temperatura de la GPU: {temperature} °C")
        except pynvml.NVMLError as e:
            ui.message(f"Error obteniendo la temperatura de la GPU: {str(e)}")

    @scriptHandler.script(
        description="Anuncia el consumo de energía de la GPU",
        gesture="kb:NVDA+shift+p"
    )
    def script_sayGPUPowerUsage(self, gesture):
        try:
            handle = pynvml.nvmlDeviceGetHandleByIndex(0)
            power_usage = pynvml.nvmlDeviceGetPowerUsage(handle) / 1000.0
            ui.message(f"Consumo de energía de la GPU: {power_usage:.2f} W")
        except pynvml.NVMLError as e:
            ui.message(f"Error obteniendo el consumo de energía de la GPU: {str(e)}")