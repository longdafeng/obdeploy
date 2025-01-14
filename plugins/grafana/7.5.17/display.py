# coding: utf-8
# OceanBase Deploy.
# Copyright (C) 2021 OceanBase
#
# This file is part of OceanBase Deploy.
#
# OceanBase Deploy is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# OceanBase Deploy is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with OceanBase Deploy.  If not, see <https://www.gnu.org/licenses/>.

from __future__ import absolute_import, division, print_function

import socket

stdio = None


def display(plugin_context, cursor, *args, **kwargs):
    stdio = plugin_context.stdio
    cluster_config = plugin_context.cluster_config
    servers = cluster_config.servers
    results = []

    for server in servers:
        server_config = cluster_config.get_server_conf(server)
        api_cursor = cursor.get(server)

        ip = server.ip
        if ip == '127.0.0.1':
            hostname = socket.gethostname()
            ip = socket.gethostbyname(hostname)
        user = api_cursor.user
        protocol = api_cursor.protocol
        if 'prometheus' in cluster_config.depends:
            url = '%s://%s:%s/d/oceanbase' % (protocol, ip, server_config['port'])
        else:
            url = '%s://%s:%s' % (protocol, ip, server_config['port'])
        stdio.verbose('type: %s'% type(server.ip))
        results.append({
            'user': user,
            'password': api_cursor.password,
            'url': url,
            'status': 'active' if api_cursor and api_cursor.connect(stdio) else 'inactive'
        })

    stdio.print_list(results, [ 'url', 'user', 'password', 'status'], lambda x: [x['url'], x['user'], x['password'], x['status']], title='grafana')
    return plugin_context.return_true()