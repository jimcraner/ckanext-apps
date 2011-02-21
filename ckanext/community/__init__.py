# this is a namespace package
try:
    import pkg_resources
    pkg_resources.declare_namespace(__name__)
except ImportError:
    import pkgutil
    __path__ = pkgutil.extend_path(__path__, __name__)

import os
from logging import getLogger

from sqlalchemy import engine_from_config

from ckan.plugins import implements, SingletonPlugin
from ckan.plugins import IRoutes, IConfigurer

from ckanext.community.model import init_model

log = getLogger(__name__)
    
class Community(SingletonPlugin):
    
    implements(IRoutes, inherit=True)
    implements(IConfigurer, inherit=True)
        
    def after_map(self, map):
        map.resource('app', 'ckanext.community.controllers.application:AppController')
        map.resource('idea', 'ckanext.community.controllers.idea:IdeaController')
        return map

    def update_config(self, config):
        """We use update_config here to get the main config from the
        application and create our extensions engine and metadata as well as
        test our templates and public folders for the extension.
        """
        engine = engine_from_config(config, 'sqlalchemy.', pool_threadlocal=True)
        init_model(engine)
         
        here = os.path.dirname(__file__)
        rootdir = os.path.dirname(os.path.dirname(here))

        template_dir = os.path.join(rootdir, 'templates')
        public_dir = os.path.join(rootdir, 'public')
        
        config['extra_template_paths'] = ','.join([template_dir,
                config.get('extra_template_paths', '')])
        config['extra_public_paths'] = ','.join([public_dir,
                config.get('extra_public_paths', '')])

