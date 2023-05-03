// 获取访问者的IP地址并显示在页面上
function getIPAddress() {
  fetch('https://api.ipify.org?format=json')
    .then(response => response.json())
    .then(data => {
      const ipAddress = data.ip;
      document.getElementById('ip-address').textContent = ipAddress;
      // 在此处将IP地址发送到服务器记录日志
    })
    .catch(error => console.error(error));
}

// 在页面加载完毕后调用getIPAddress函数
window.addEventListener('load', getIPAddress);
