# WXS implementation
This drb-impl-wXs module implements the OWS services (WFS, WMS, WCS, ...). 
For more information about OWS Service see https://www.ogc.org/ or/and
https://www.ogc.org/standards/wms
OGC catalog, this implementation is abstract, it means that to have a usable 
OWS service implementation, we have to create an implementation for this service 
dependent on this abstract implementation.
Sot have a signature, its derived implementations will have to define one

# Nodes
### WXSServiceNode
Abstract, have to be derived.
Represents the WXS service (like WMS, WCS, ...). This node has no attribute and
has as children request (like GetMap) WXsOperationNode and other children that
define the Service as XmlNode

### WXSNodeOperation
Represents an operation than can be used on the service.


# Installation
```
pip install drb-impl-wxs
```
# Usages

To implement an OWS Web Service, we have to create a class based on  WXSServiceNode
and define at least the read_capabilities method.

```python
class WmsServiceNode(WXSServiceNode):
    ...
    def read_capabilities(self, node_capabilities):
        ....
    
```


After we can use this node like other DRB Node
The operation of service are available across the children of the node service,
See drb_impl_wms for more information.

```python
get_map = service_wms['GetMap'][predicate]

```






