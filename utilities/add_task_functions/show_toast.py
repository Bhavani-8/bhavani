def show_toast(driver, message):
    script = f"""
        var toast = document.createElement('div');
        toast.innerText = `{message}`;
        toast.style.position = 'fixed';
        toast.style.bottom = '10px';
        toast.style.right = '10px'; 
        toast.style.backgroundColor = 'black';
        toast.style.color = 'white';
        toast.style.padding = '10px';
        toast.style.zIndex = 10000;
        document.body.appendChild(toast);
        setTimeout(() => toast.remove(), 3000);
        """
    driver.execute_script(script)
