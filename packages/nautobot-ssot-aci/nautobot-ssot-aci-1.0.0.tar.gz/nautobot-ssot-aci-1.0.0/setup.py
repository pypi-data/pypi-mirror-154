# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nautobot_ssot_aci',
 'nautobot_ssot_aci.diffsync',
 'nautobot_ssot_aci.diffsync.adapters',
 'nautobot_ssot_aci.diffsync.models',
 'nautobot_ssot_aci.tests']

package_data = \
{'': ['*'],
 'nautobot_ssot_aci': ['static/nautobot_ssot_aci/*'],
 'nautobot_ssot_aci.diffsync': ['device-types/*']}

install_requires = \
['Jinja2<3',
 'PyYAML>=5.4.1,<6.0.0',
 'diffsync>=1.3.0,<2.0.0',
 'nautobot-ssot>=1.0.1,<2.0.0']

extras_require = \
{':extra == "nautobot"': ['nautobot>=1.2.5,<2.0.0']}

setup_kwargs = {
    'name': 'nautobot-ssot-aci',
    'version': '1.0.0',
    'description': 'Nautobot SSoT for Cisco ACI',
    'long_description': '# Nautobot SSoT ACI - Nautobot plugin for synchronizing with Cisco ACI\n\nNautobot SSoT ACI is a plugin for [Nautobot](https://github.com/nautobot/nautobot) allowing synchronization of data from Cisco ACI into Nautobot.\n\nThis plugin is built on top of the [Nautobot Single Source of Truth (SSoT)](https://github.com/nautobot/nautobot-plugin-ssot) plugin. SSoT plugin enables Nautobot to be the aggregation point for data coming from multiple systems of record (SoR).\n\nTo accomplish the synchronization of data, the SSoT ACI plugin communicates with the Cisco ACI controller, the Application Policy Infrastructure Controller (APIC). The APIC provides a central point of administration for the ACI fabric via a web dashboard or REST API.\n\nThe SSoT ACI plugin eliminates the need for manually adding objects to Nautobot that have been automatically discovered by the Cisco APIC controller.  This includes information such as device model/serial numbers, node management IP addressing, and more.\n\nIn addition any changes to the ACI fabric are reflected in Nautobot when the synchronization process is executed.\n\nExamples of ACI changes synchronized into Nautobot:\n\n- New devices that were registered to the fabric are added to Nautobot.\n- Devices decommissioned from the fabric are removed from Nautobot.\n- Management IP addresses of devices added to the ACI fabric are created in Nautobot.\n- Subnets and gateway addresses of bridge domains created in ACI are added to Nautobot as prefixes and IP addresses.\n- Prefixes and IP addresses associated with removed ACI bridge domains are deleted from Nautobot.\n- ACI interface description additions and updates are carried over to interface descriptions in Nautobot.\n\nThe below list shows object types that are currently synchronized and how they map between systems.\n\n| **ACI**                                       \t| **Nautobot**                  \t|\n|-----------------------------------------------\t|-------------------------------\t|\n| Tenant                                        \t| Tenant                        \t|\n| Node (Leaf/Spine/Controller)                  \t| Device                        \t|\n| Model                                         \t| Device Type                   \t|\n| Management IP address (Leaf/Spine/Controller) \t| IP Address                    \t|\n| Bridge Domain Subnet                          \t| Prefix, IP Address              |\n| Interfaces                                    \t| Interface \t                    |\n| VRFs                                            | VRFs                            |\n\n## Documentation\n\nDocumentation is hosted on ReadTheDocs at [Nautobot SSoT for Cisco ACI Documentation](https://nautobot-plugin-ssot-aci.readthedocs.io/).\n\n## Screenshots\n\n![ACI Job Landing Page](https://user-images.githubusercontent.com/6945229/162988513-c71fcd06-8cc7-46ac-92bf-5895cde10c81.png)\n![ACI Job Options Page](https://user-images.githubusercontent.com/6945229/155608556-22eade64-8289-4e20-82a4-e2f4e15809f4.png)\n![ACI Job Post-Run Page](https://user-images.githubusercontent.com/6945229/155609055-1d93335b-53b1-4fd8-bf1b-58d64b970f1e.png)\n![ACI Synchronization Details](https://user-images.githubusercontent.com/6945229/155609222-c720f23f-4af8-4659-a5af-83bc69466d07.png)\n![Imported Device with ACI Attributes](https://user-images.githubusercontent.com/6945229/155609612-34bdcfea-bde2-4924-8de0-3cf74796d744.png)\n![Imported IPs with ACI Attributes](https://user-images.githubusercontent.com/6945229/155609826-d3938767-6287-4626-94a3-aea4fd758204.png)\n![Imported Prefixes with ACI Attributes](https://user-images.githubusercontent.com/6945229/155610226-799c79de-719b-44af-9a07-2aaabfea5510.png)\n\n\n## Contributing\n\nPull requests are welcomed and automatically built and tested against multiple version of Python and multiple version of Nautobot through TravisCI.\n\nThe project is packaged with a light development environment based on `docker-compose` to help with the local development of the project and to run the tests within TravisCI.\n\nThe project is following Network to Code software development guideline and is leveraging:\n\n- Black, Pylint, Bandit and pydocstyle for Python linting and formatting.\n- Django unit test to ensure the plugin is working properly.\n\n\n## Questions\n\nFor any questions or comments, please check the [FAQ](FAQ.md) first and feel free to swing by the [Network to Code slack channel](https://networktocode.slack.com/) (channel #networktocode).\nSign up [here](http://slack.networktocode.com/)\n',
    'author': 'Network to Code, LLC',
    'author_email': 'info@networktocode.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/nautobot/nautobot-plugin-ssot-aci',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
