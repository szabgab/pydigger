% include('incl/header.tpl')
<h2>{{name}}</h2>
<ul>
% for p in pkgs:
  <li>{{p['version']}}</li>
% end
</ul>

<h2>Files of {{pkgs[0]['version']}}</h2>
<ul>
% if 'files' in pkgs[0]:
%     for f in pkgs[0]['files']:
          <li><a href="/package/">{{f}}</a></li>
%     end
% else:
      No files were recorded
% end
</ul>

% include('incl/footer.tpl')

