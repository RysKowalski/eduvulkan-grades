
// getLessons.js
const { Keypair, VulcanHebeCe, VulcanJwtRegister } = require("hebece")

const fs = require('fs');

const APIAP = fs.readFileSync('token.txt', 'utf8')
async function main() {
  // 2) generate keypair
  const kpManager = new Keypair();
  const keypair = await kpManager.init();
  console.log("Keypair fingerprint:", keypair.fingerprint);

  // 3) register JWT
  const jwtReg = new VulcanJwtRegister(keypair, APIAP, true);
  await jwtReg.init();
  console.log("JWT registered");

  // 4) connect to Hebe
  const heb = new VulcanHebeCe(keypair);
  await heb.connect();

  console.log("Students:");
  console.log(heb.students);

  // 5) select first student automatically
  await heb.selectStudent();

  console.log(
    "Selected:",
    heb.selectedStudent.FirstName,
    heb.selectedStudent.LastName
  );


  const now = new Date();

  // Monday as start of week
  const day = now.getDay() === 0 ? 7 : now.getDay();

  const dateFrom = new Date(now);
  dateFrom.setDate(now.getDate() - (day - 1));
  dateFrom.setHours(0, 0, 0, 0);

  const dateTo = new Date(now);
  dateTo.setDate(now.getDate() + (7 - day));
  dateTo.setHours(23, 59, 59, 999);

  console.log(dateFrom, dateTo);
  // 7) fetch lessons
  const resp = await heb.getGrades(dateFrom, dateTo);

  json = JSON.stringify(resp.Envelope, null, 2);
  fs.writeFileSync('test.json', json, 'utf8')

}

main().catch(err => {
  console.error(err);
});
