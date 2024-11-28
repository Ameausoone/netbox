
from extras.validators import CustomValidator
from ipaddress import ip_address, IPv4Address

from netaddr.ip import IPNetwork


class DNSRecordValidator(CustomValidator):

    def validate(self, instance, request):
        """
        Validate a DNS record before saving.
        """
        #print("Instance:", vars(instance))
        #print("Request:", vars(request))
        #try:
        #    from netbox_dns.models import Zone
        #    query_zones = Zone.objects.filter(
        #        id=instance.zone_id
        #    )
        #    zone = query_zones.first()
        #    #print("Zone:", vars(zone))
#
        #except Exception as e:
        #    print("Exception:", e)
        #    self.fail("The associated zone does not exist.", field='zone')

        # Forbidden other record types than A and CNAME
        if instance.type not in ["A", "CNAME", "SOA"]:
            self.fail("Only A and CNAME record types are allowed.", field='type')

        # Validate the value format based on the record type
        if instance.type == "A":
            # check if the ip
            ip = None
            try:
                ip = ip_address(instance.value)
            except ValueError:
                self.fail("The value field must be a valid IPv4 address for A records.", field='value')
            if ip is None or not isinstance(ip,IPv4Address):
                self.fail("The Value field must be a valid IPv4 address for A records.", field='value')
            if ip.is_private:
                if instance.cf["cust_vrf_id"] is None:
                    self.fail("The VRF field is required for private IP addresses.", field='vrf_id')
                vrf_id = instance.cf["cust_vrf_id"]
                from ipam.models.vrfs import VRF
                queryset = VRF.objects.filter(id=vrf_id)
                if queryset.count() == 0:
                    self.fail("The provided VRF ID doesn't exist.", field='vrf_id')
                vrf = queryset.first()
                from ipam.models.ip import Prefix
                queryset = Prefix.objects.filter(vrf_id=vrf.id)
                isIpInVrf = False
                for entry in queryset:
                    print("Prefix:",vars(entry))
                    ip = IPNetwork(entry.prefix)
                    if ip.ip == ip_address(instance.value):
                        isIpInVrf = True
                        break
                if not isIpInVrf:
                    self.fail("The provided ip is not in VRF.", field='value')


        elif instance.type == "CNAME":
            if not instance.value.endswith("."):
                self.fail("The value field must end with a dot ('.') for CNAME records.", field='value')

