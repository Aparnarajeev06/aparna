from django.db import models
from django.contrib.auth.models import User
from products.models import Product

class PCBuild(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="pc_builds")
    name = models.CharField(max_length=100, default="My Custom Rig")
    cpu = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, related_name="build_cpus")
    motherboard = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, related_name="build_motherboards")
    ram = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, related_name="build_rams")
    gpu = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, related_name="build_gpus")
    storage = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, related_name="build_storages")
    psu = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True, related_name="build_psus")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.user.username if self.user else 'Guest'}"

    @property
    def total_price(self):
        total = 0
        for component in [self.cpu, self.motherboard, self.ram, self.gpu, self.storage, self.psu]:
            if component:
                total += component.price
        return total

    @property
    def total_wattage(self):
        total_draw = 0
        for component in [self.cpu, self.gpu, self.ram, self.storage]:
            if component:
                total_draw += component.wattage
        return total_draw

    @property
    def is_compatible(self):
        # Socket compatibility check
        if self.cpu and self.motherboard:
            if self.cpu.socket_type.lower() != self.motherboard.socket_type.lower():
                return False
        # Memory type check
        if self.motherboard and self.ram:
            if self.motherboard.ram_type.lower() != self.ram.ram_type.lower():
                return False
        # Wattage capacity check
        if self.psu:
            if self.total_wattage > self.psu.wattage:
                return False
        return True
