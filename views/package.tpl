% include('incl/header.tpl')
<h2>{{name}}</h2>
<ul>
% for p in pkgs:
  <li>{{p['version']}}</li>
% end
</ul>
% include('incl/footer.tpl')

