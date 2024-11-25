
from extras.validators import CustomValidator
from ipaddress import ip_address

class DNSRecordValidator(CustomValidator):

    def validate(self, instance, request):
        """
        Validate a DNS record before saving.
        """
        try:
            from netbox_dns.models import Zone
            query_zones = Zone.objects.filter(
                id=instance.zone_id
            )
            zone = query_zones.first()

            print("Zone:", vars(zone))
            # TODO implement some coherence tests against zone information
        except Exception as e:
            print("Exception:", e)
            self.fail("The associated zone does not exist.", field='zone')

        # Forbidden other record types than A and CNAME
        if instance.type not in ["A", "CNAME","SOA"]:
            self.fail("Only A and CNAME record types are allowed.", field='type')

        # Validate the value format based on the record type
        if instance.type == "A":
            try:
                ip_address(instance.value)
            except ValueError:
                self.fail("The value field must be a valid IPv4 address for A records.", field='value')

        elif instance.type == "CNAME":
            if not instance.value.endswith("."):
                self.fail("The value field must end with a dot ('.') for CNAME records.", field='value')

