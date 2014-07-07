% include('incl/header.tpl', title = "Stats")
Total number of packages {{pkg_count}}<br />

<ul>
% for s in statuses:
    <li>{{s}} {{statuses[s]}}</li>
% end
</ul>

% include('incl/footer.tpl')

