import { useState } from "react";

function BaconDistance() {
  const [distance, setDistance] = useState("");
  const [computedDistance, setComputedDistance] = useState(false);
  const [actor, setActor] = useState("");

  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setActor(event.target.value);
  };

  const handleSumbit = (event: React.MouseEvent<HTMLButtonElement>) => {
    const url = "http://127.0.0.1:5000/" + actor;
    fetch(url)
      .then((response) => response.text())
      .then((data) => {
        setDistance(data);
      });
    setComputedDistance(true);
    setActor("");
  };

  return (
    <>
      <h1>Bacon Distance</h1>
      <input
        type="text"
        value={actor}
        onChange={handleChange}
        placeholder="Type actor name"
      />
      <button onClick={handleSumbit}>sumbit</button>
      <p style={{color:"red"}} hidden={!computedDistance} >Distance is {distance}</p>
    </>
  );
}

export default BaconDistance;
