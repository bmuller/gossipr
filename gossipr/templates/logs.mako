<%inherit file="base.mako"/>
<section>
  <h1>Chat Logs: ${room.name}</h1>
  <article class="span-20">
    <div id="qform">
      <form action="/">
	<span>Query: <input type="text" name="query" value="${query}" /></span>
	<span>Start Date: <input size="13" type="text" id="startdate" value="${startdate}" name="startdate" /></span>
	<span>End Date: <input size="13" type="text" id="enddate" value="${enddate}" name="enddate" /></span>
	<input type="submit" class="button second medium" value="Search" />
	<input type="hidden" name="room_id" value="${room.id}" />
      </form>
    </div>
    <script type="text/javascript">$('#startdate').datetimepicker({ dateFormat: 'yy-mm-dd' })</script>
    <script type="text/javascript">$('#enddate').datetimepicker({ dateFormat: 'yy-mm-dd' });</script>
    <table>
      <tr>
	<th scope="col">speaker</th>
	<th scope="col">time</th>
	<th scope="col">message</th>
      </tr>
% for msg in msgs:
      <tr>
	<td>${msg['speaker']}</td>
	<td>${msg['created_at']}</td>
	<td>${msg['msg']}</td>
      </tr>
% endfor
    </table>
  </article>
</section>
<%def name="title()">
Chat Logs: ${room.name}
</%def>
