export function ajaxRequest(url, data, type = 'GET', cache = true, contentType = 'application/x-www-form-urlencoded; charset=UTF-8', processData = true) {
    return new Promise((resolve, reject) => {
        $.ajax({
            url: url,
            type: type,
            cache: cache,
            contentType: contentType,
            processData: processData,
            data: data,
            headers: token,
            success: function (data) {
                resolve(data);
            },
            error: reject
        });
    });
}