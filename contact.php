<?php

require 'PHPMailer/PHPMailerAutoload.php';
require 'config.php';

$name=$email=$message=$subject_type="";

$name = $_POST["name"];
$email = $_POST["email"];
$message=$_POST["message"];
$subject_type=$_POST["select_type"];

$mail = new PHPMailer;

if( $mail_type === 1 ) {
    //sendmail is chosen
    $mail->isSendmail();
}

elseif ($mail_type === 2){
    //smtp is chosen
    $mail->isSMTP();
    }
    $mail->Host = $host_name;
    $mail->SMTPAuth = true;
    $mail->Username = $user_name;
    $mail->Password = $password;
    $mail->SMTPSecure = 'tls';
    $mail->Port = $port;
    $mail->Subject = $subject;
    $mail->setFrom($email, 'User');
    $mail->addAddress($to_email,$to_name);
    $mail->Subject = 'Contact us - Astrology';
    $mail->Body = 'Name: ' . $name . '<br>Email: ' . $email . '<br>Message: ' . $message .'<br>Subject Type: ' .$subject_type;


if (!$mail->send()) {
    echo 'Email could not be sent.';
    echo 'Mailer Error: ' . $mail->ErrorInfo;
} else {
//    echo 'Email has been sent';
    header("Location: " . $_SERVER["HTTP_REFERER"]);

   /* ?>
    <script type="text/javascript">
        alert("Success, We sent you an email.");
        history.back();
    </script>
    <?php
    */
}