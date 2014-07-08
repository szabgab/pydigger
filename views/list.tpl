% include('incl/header.tpl', title='PyDigger')
<ul>
% for p in pkgs:
  <li><a href="/package/{{p}}">{{p}}</a></li>
% end
</ul>
% include('incl/footer.tpl')
