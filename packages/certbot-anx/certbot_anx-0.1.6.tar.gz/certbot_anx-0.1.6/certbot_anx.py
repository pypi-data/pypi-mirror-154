import logging
import zope.interface

from certbot.plugins.dns_common import DNSAuthenticator
from certbot.interfaces import IAuthenticator, IPluginFactory
from datetime import datetime, timedelta
from time import sleep
from pyanxdns import Client, split_domain


logger = logging.getLogger(__name__)


@zope.interface.implementer(IAuthenticator)
@zope.interface.provider(IPluginFactory)
class ANXAuthenticator(DNSAuthenticator):
    """
    ANX DNS ACME authenticator.
    This Authenticator uses the Loopia API to fulfill a dns-01 challenge.
    """

    #: Short description of plugin
    description = __doc__.strip().split("\n", 1)[0]

    #: TTL for the validation TXT record
    ttl = 30

    def __init__(self, *args, **kwargs):
        super(ANXAuthenticator, self).__init__(*args, **kwargs)
        self._client = None
        self.credentials = None

    @classmethod
    def add_parser_arguments(cls, add, default_propagation_seconds=0.5 * 60):
        super(ANXAuthenticator, cls).add_parser_arguments(
            add, default_propagation_seconds)
        add("credentials", help="ANX API credentials INI file.")


    def more_info(self):
        """
        More in-depth description of the plugin.
        """

        return "\n".join(line[4:] for line in __doc__.strip().split("\n"))

    def _setup_credentials(self):
        self.credentials = self._configure_credentials(
            "credentials",
            "ANX credentials INI file",
            {
                "apikey": "API key for ANX account"
            },
        )

    def _get__client(self, domain):
        return Client(
            domain,
            self.credentials.conf("apikey")
        )

    def _perform(self, domain, validation_name, validation):
        domain_parts = split_domain(validation_name)
        client = self._get__client(domain_parts.domain)

        name = validation_name
        if not name.endswith('.'):
            name = name + '.'

        logger.debug(
            "Creating TXT record for {} on subdomain {}".format(*domain_parts))
        
        logger.debug(
            "Creating TXT record for {}".format(name ))

        client.add_txt_record(name, validation,ttl=self.ttl)

    def _cleanup(self, domain, validation_name, validation):
        domain_parts = split_domain(validation_name)
        client = self._get__client(domain_parts.domain)

        msg = "Removing subdomain {1} on subdomain {0}"
        logger.debug(msg.format(*domain_parts))

        client.delete_by_txt(validation, name=validation_name + ".")