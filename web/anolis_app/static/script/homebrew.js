<script type=text/javascript>
	$SCRIPT_ROOT = {{ request.script_root|tojson|safe }};
</script>
	
<script type=text/javascript>
  $(function() {
    $('#submit_msats').bind('click', function() {
      $.getJSON($SCRIPT_ROOT + '/query_result', {
      	size: $("input[name='size']").val(),
      	length: $("length[name='length']").val(),
      	combine_loci: $("combine_loci[name='combine_loci']").val(),
      	tag_primers: $("tag_primers[name='tag_primers']").val(),
      	}, function(data) {
        $("#test_result").text(data.result);
      });
      return false;
    });
  });
</script>