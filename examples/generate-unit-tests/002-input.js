function isAdult(age) {
  if (typeof age !== 'number') return false;
  return age >= 18;
}
module.exports = isAdult;
