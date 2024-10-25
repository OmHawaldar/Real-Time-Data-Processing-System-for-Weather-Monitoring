import nodemailer from 'nodemailer';

// List of users' emails
const users = [
  { name: 'John Doe', email: 'omh1ga22is407@gmail.com' },
  { name: 'Jane Doe', email: 'user2@example.com' },
  { name: 'Alice', email: 'user3@example.com' }
];

// Create a transporter object using Gmail SMTP
const transporter = nodemailer.createTransport({
  service: 'gmail',
  auth: {
    user: 'hawaldarom39@gmail.com',  // Replace with your Gmail account
    pass: 'qray hvrn xtpe hsfv',   // Replace with your Gmail password or App Password
  },
});

// Loop through each user and send a personalized email
users.forEach(user => {
  const mailOptions = {
    from: 'your_email@gmail.com',       // Sender's address
    to: user.email,                     // Recipient's address
    subject: 'Personalized Weather Alert', // Subject of the email
    text: `Hello ${user.name},\n\nSevere weather conditions detected. Stay safe!`, // Personalized message
  };

  transporter.sendMail(mailOptions, (error, info) => {
    if (error) {
      return console.log(`Error sending to ${user.email}:`, error);
    }
    console.log(`Email sent to ${user.name} (${user.email}): ` + info.response);
  });
});
