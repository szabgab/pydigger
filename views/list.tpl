% include('incl/header.tpl', title='PyDigger')
<ul>
% for p in pkgs:
  <li>{{p['package']}}</li>
% end
</ul>
% include('incl/footer.tpl')
