import pynetbox
import pytest


def test_create_dns_record_other_than_a_or_cname(nb: pynetbox.api):
    # Create a DNS record with a type other than A or CNAME
    zone = nb.plugins.netbox_dns.zones.get(name='app.dkt.cloud')
    with pytest.raises(pynetbox.RequestError) as excinfo:
        nb.plugins.netbox_dns.records.create(name='test', zone =zone.id, type= 'MX', value='10 mail.example.com.')
    assert "Only A and CNAME record types are allowed." in str(excinfo.value)

def test_create_dns_record_a_with_invalid_value(nb: pynetbox.api):
    # Create a DNS record with type A and an invalid value
    zone = nb.plugins.netbox_dns.zones.get(name='app.dkt.cloud')
    with pytest.raises(pynetbox.RequestError) as excinfo:
        nb.plugins.netbox_dns.records.create(name='test', zone =zone.id, type= 'A', value='123431243')
    assert "is not a valid value for" in str(excinfo.value)

def test_create_dns_record_a_with_private_ip_and_without_vrf(nb: pynetbox.api):
    zone = nb.plugins.netbox_dns.zones.get(name='app.dkt.cloud')
    res = None
    with pytest.raises(pynetbox.RequestError) as excinfo:
        res = nb.plugins.netbox_dns.records.create(name='test', zone =zone.id, type= 'A', value='10.10.10.24')
    print("##res:",res)
    assert "The VRF field is required for" in str(excinfo.value)

def test_create_dns_record_a_with_unexistent_vrf(nb: pynetbox.api):
    zone = nb.plugins.netbox_dns.zones.get(name='app.dkt.cloud')
    with pytest.raises(pynetbox.RequestError) as excinfo:
        nb.plugins.netbox_dns.records.create(name='test', zone =zone.id, type= 'A', custom_fields={"cust_vrf_id":1234}, value='10.10.10.24')
    assert "The provided VRF ID doesn't exist" in str(excinfo.value)

def test_create_dns_record_a_with_private_address_not_in_vrf(nb: pynetbox.api):
    zone = nb.plugins.netbox_dns.zones.get(name='app.dkt.cloud')
    vrf = nb.ipam.vrfs.get(name='ecomm-inter-staging')
    with pytest.raises(pynetbox.RequestError) as excinfo:
        nb.plugins.netbox_dns.records.create(name='test', zone =zone.id, type= 'A', value='10.10.10.24',custom_fields={"cust_vrf_id":vrf.id})
    assert "The provided ip is not in VRF" in str(excinfo.value)
    #nb.plugins.netbox_dns.records.delete(name='test')


