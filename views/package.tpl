% include('incl/header.tpl')
<h2>{{name}} {{pkgs[idx]['version']}}</h2>
<div id="pypi_json_link">
<a href="http://pypi.python.org/pypi/{{name}}/{{pkgs[idx]['version']}}/json">PyPi JSON</a>
</div>

<input type="hidden" id="package_name" value="{{name}}" />

<select id="version_selector" name="idx">
  <option value="">Select Verion</option>
% for i in range(0, len(pkgs)):
%   if i != idx:
       <option value="{{pkgs[i]['version']}}">{{pkgs[i]['version']}} at {{pkgs[i]['upload_time'] if 'upload_time' in pkgs[i] else  ''}}</option>
%   end
% end
</select><br>
<button id="jump_to">Jump to</button>
<!-- <button id="diff_with">Diff with</button> -->

<h2>Files</h2>
<ul>
% if 'files' in pkgs[idx]:
%     for f in pkgs[idx]['files']:
%         if 'project_path' in pkgs[idx]:
              <li><a href="/{{pkgs[idx]['project_path']}}/{{f}}">{{f}}</a></li>
%         else:
              <li>{{f}}</li>
%         end
%     end
% else:
      No files were recorded
% end
</ul>

% include('incl/footer.tpl')

