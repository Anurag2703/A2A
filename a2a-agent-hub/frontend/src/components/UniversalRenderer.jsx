import React from "react";
import "./UniversalRenderer.css";

const UniversalRenderer = ({ data }) => {
  if (!data) return null;

  // 1️⃣ If API follows AUI protocol and wraps in `content.data`, unwrap it
  if (data?.content?.data) {
    return <UniversalRenderer data={data.content.data} />;
  }

  // 2️⃣ If API just returned plain JSON inside `output`, unwrap that too
  if (data?.output?.content?.data) {
    return <UniversalRenderer data={data.output.content.data} />;
  }

  // 3️⃣ If data is a string, render as preformatted text
  if (typeof data === "string") {
    return <p className="whitespace-pre-wrap">{data}</p>;
  }

  // 4️⃣ If primitive value
  if (typeof data !== "object") {
    return <p>{String(data)}</p>;
  }

  // 5️⃣ If array, render each item
  if (Array.isArray(data)) {
    return (
      <ul className="list-disc pl-6">
        {data.map((item, idx) => (
          <li key={idx}>
            <UniversalRenderer data={item} />
          </li>
        ))}
      </ul>
    );
  }

  // 6️⃣ Object rendering (table-like)
  return (
    <table className="border border-gray-300 border-collapse w-full">
      <tbody>
        {Object.entries(data).map(([key, value], idx) => (
          <tr key={idx} className="border border-gray-300 align-top">
            <td className="font-semibold p-2 border border-gray-300 bg-gray-50 w-1/4">
              {key}
            </td>
            <td className="p-2 border border-gray-300">
              <UniversalRenderer data={value} />
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
};

export default UniversalRenderer;




// import React from "react";

// const UniversalRenderer = ({ data }) => {
//   if (!data) return null;

//   // If data is a string, just show it
//   if (typeof data === "string") {
//     return <p className="whitespace-pre-wrap">{data}</p>;
//   }

//   // If data is a number, boolean, or null
//   if (typeof data !== "object") {
//     return <p>{String(data)}</p>;
//   }

//   // If data is an array
//   if (Array.isArray(data)) {
//     return (
//       <ul className="list-disc pl-6">
//         {data.map((item, idx) => (
//           <li key={idx}>
//             <UniversalRenderer data={item} />
//           </li>
//         ))}
//       </ul>
//     );
//   }

//   // If data is an object (table-like display)
//   return (
//     <table className="border border-gray-300 border-collapse">
//       <tbody>
//         {Object.entries(data).map(([key, value], idx) => (
//           <tr key={idx} className="border border-gray-300">
//             <td className="font-semibold p-2 border border-gray-300 bg-gray-50">
//               {key}
//             </td>
//             <td className="p-2 border border-gray-300">
//               <UniversalRenderer data={value} />
//             </td>
//           </tr>
//         ))}
//       </tbody>
//     </table>
//   );
// };

// export default UniversalRenderer;
