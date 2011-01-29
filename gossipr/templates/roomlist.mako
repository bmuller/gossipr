<%inherit file="base.mako"/>
<section>
  <h1>Chat Logs: awesome title (2)</h1>
  <article class="span-20">
    <ul>
% for name, url in links.items():
      <li><a href="${url}">${name}</a></li>
% endfor 
    </ul>
  </article>
</section>

<%def name="title()">
Room List
</%def>
