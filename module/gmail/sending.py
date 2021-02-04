def kirim(p,s,t):
    import smtplib
    from email.mime.text import MIMEText as text

    server=smtplib.SMTP_SSL("smtp.gmail.com",465)  # inisualisasi objects smtplib (SMTP_SSL)
    server.login("jekomontainugrah@gmail.com","120599$3") # login ke email 

    m = text(p) # membuat teks message
    m['Subject'] = s # object messege to email

    # kirim email index[0] email pengirim,index[1] email penerima,index[2]pesan dan objeck 
    server.sendmail("jekomontainugrah@gmail.com",t,m.as_string())
    # tutup server
    server.quit()
    
