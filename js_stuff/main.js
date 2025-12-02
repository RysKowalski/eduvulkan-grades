
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


  const resp = await heb.getGrades();

  json = JSON.stringify(resp.Envelope, null, 2);
  fs.writeFileSync('../raw.json', json, 'utf8')

}

main().catch(err => {
  console.error(err);
});
