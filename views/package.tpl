% include('incl/header.tpl')
<h2>{{name}}</h2>
<ul>
% for p in pkgs:
  <li>{{p['version']}} on {{p['upload_time'] if 'upload_time' in p else  ''}}  <a href="http://pypi.python.org/pypi/{{p['package']}}/{{p['version']}}/json">PyPi JSON</a></li>
% end
</ul>

<h2>Files of {{pkgs[0]['version']}}</h2>
<ul>
% if 'files' in pkgs[0]:
%     for f in pkgs[0]['files']:
%         if 'project_path' in pkgs[0]:
              <li><a href="/{{pkgs[0]['project_path']}}/{{f}}">{{f}}</a></li>
%         else:
              <li>{{f}}</li>

%         end
%     end
% else:
      No files were recorded
% end
</ul>

% include('incl/footer.tpl')

