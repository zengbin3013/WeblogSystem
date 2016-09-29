$(document).ready(function () {
    var d = new Date();
    d.setTime(d.getTime()-24*60*60*1000);
    var yestoday = d.getFullYear()+"-" + (d.getMonth()+1) + "-" + d.getDate();
    $('#sdatepicker').datetimepicker({
        autoclose:true,
        startView: 'month',
        minView:'month',
        language: 'zh-CN',
        tomonthHighlight:true,
        format: 'yyyy-mm-dd',
        endDate: yestoday
    });
    $('#sdatepicker').datetimepicker().on('changeDate', function (ev) {
        var newDate = new Date();
        newDate.setTime(ev.date.valueOf());
        
        strDate = newDate.getFullYear() + '-' + (newDate.getMonth() + 1) + '-' + newDate.getDate();
        var edate = new Date($('#edatepicker').val()).getTime();
        if (ev.date.valueOf() > edate) {
            $('#edatepicker').val(strDate);
            $('#edatepicker').datetimepicker('update');
        }
        $('#edatepicker').datetimepicker('setStartDate', strDate);
    });
    $('#edatepicker').datetimepicker({
        autoclose: true,
        language: 'zh-CN',
        startView: 'month',
        minView: 'month',
        tomonthHighlight: true,
        format: 'yyyy-mm-dd',
        startDate: yestoday,
        endDate:yestoday
    });
    $(function () {
        var options = {
            //lines: { show: true, fill: true },
            points:{show:true},
            xaxis: {
                mode: "time",
                tickFormatter: function (val, axis) {
                    var d = new Date(val);
                    if (d.getHours() == 0) {
                        return d.getMonth() + '-' + d.getDate() + ' ' + d.getHours() + ':00';
                    }
                    else {
                        return d.getMonth() + '-' + d.getDate() + ' ' + d.getHours() + ':00';
                    }
                    //return d.toLocaleTimeString();//转为当地时间格式  
                }
            }
        };
        $.plot("#flot-line-chart", [
            { label: "访问总次数", data: visit_total, lines: { show: true, fill: true } },
            { label: "code20x次数", data: visit_20x, lines: { show: true, fill: false } },
            { label: "code30x次数", data: visit_30x, lines: { show: true, fill: false } },
            { label: "code40x次数", data: visit_40x, lines: { show: true, fill: false } },
            { label: "code50x次数", data: visit_50x, lines: { show: true, fill: false } }
        ], options);
    });
    $('#btnsearch').click(function () {
        sitename = $('.selectpicker').val();
        sdate = $('#sdatepicker').val();
        edate = $('#edatepicker').val();
        data = { sitename: sitename, sdate: sdate, edate: edate }
        $.ajaxSetup({
            data: { csrfmiddlewaretoken: csrf_token },
        });
        var chart_data = [];
        var options = []
        $.plot("#flot-line-chart", chart_data, options);
        $.post('/admin/getcodedata/', data, function (d) {
            var options = {
                points: { show: true },
                xaxis: {
                    mode: "time",
                    tickFormatter: function (val, axis) {
                        var d = new Date(val);
                        if (d.getHours() == 0) {
                            return d.getMonth() + '-' + d.getDate() + ' ' + d.getHours() + ':00';
                        }
                        else {
                            return d.getMonth() + '-' + d.getDate() + ' ' + d.getHours() + ':00';
                        }
                    }
                }
            };
            if (d.errcode ==0) {
                $.plot("#flot-line-chart", [
                    { label: "访问总次数", data: d.data.visit_total, lines: { show: true, fill: true } },
                    { label: "code20x次数", data: d.data.visit_20x, lines: { show: true, fill: false } },
                    { label: "code30x次数", data: d.data.visit_30x, lines: { show: true, fill: false } },
                    { label: "code40x次数", data: d.data.visit_40x, lines: { show: true, fill: false } },
                    { label: "code50x次数", data: d.data.visit_50x, lines: { show: true, fill: false } }
                ], options);
            }
        });
    });
});